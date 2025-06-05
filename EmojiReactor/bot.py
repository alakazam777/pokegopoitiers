import discord
from discord.ext import commands
import asyncio
import logging
import os
from dotenv import load_dotenv
from config import Config
from image_analyzer import ImageAnalyzer
from emoji_mapper import EmojiMapper
import aiohttp

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('discord_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ImageReactionBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        # Remove privileged intents to avoid permission issues
        intents.message_content = False
        intents.guild_messages = True
        intents.guilds = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        self.config = Config()
        self.image_analyzer = ImageAnalyzer()
        self.emoji_mapper = EmojiMapper()
        self.session: aiohttp.ClientSession | None = None

    async def setup_hook(self):
        """Setup hook called when bot is starting up"""
        self.session = aiohttp.ClientSession()
        logger.info("Bot setup completed")

    async def close(self):
        """Cleanup when bot is shutting down"""
        if self.session:
            await self.session.close()
        await super().close()

    async def on_ready(self):
        """Called when bot is ready and connected to Discord"""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is monitoring channel: {self.config.TARGET_CHANNEL_ID}')
        
        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="for images to analyze 👁️"
        )
        await self.change_presence(activity=activity)

    async def on_message(self, message):
        """Handle incoming messages"""
        # Log all messages for debugging
        logger.info(f"Received message in channel {message.channel.id} from {message.author}")
        
        # Ignore messages from the bot itself
        if message.author == self.user:
            logger.info("Ignoring message from bot itself")
            return

        # Check if message is in the target channel
        if str(message.channel.id) != self.config.TARGET_CHANNEL_ID:
            logger.info(f"Message not in target channel. Expected: {self.config.TARGET_CHANNEL_ID}, Got: {message.channel.id}")
            return
        
        logger.info("Message is in target channel, checking for attachments")

        # Check if message contains attachments (images)
        image_attachments = [
            attachment for attachment in message.attachments
            if any(attachment.filename.lower().endswith(ext) 
                  for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp'])
        ]

        if not image_attachments:
            # Also check if message content contains image URLs (for compatibility without message_content intent)
            if hasattr(message, 'content') and message.content:
                # Only process if we can access content, otherwise skip
                pass
            return

        logger.info(f"Found {len(image_attachments)} image(s) in message from {message.author}")

        # Process each image
        for attachment in image_attachments:
            await self.process_image_attachment(message, attachment)

        # Process commands
        await self.process_commands(message)

    async def process_image_attachment(self, message, attachment):
        """Process a single image attachment"""
        try:
            logger.info(f"Processing image: {attachment.filename}")
            
            # Download image
            if self.session is None:
                logger.error("HTTP session not initialized")
                return
            async with self.session.get(attachment.url) as response:
                if response.status != 200:
                    logger.error(f"Failed to download image: {response.status}")
                    return
                
                image_data = await response.read()
            
            # Analyze image with OpenAI Vision
            analysis_result = await self.image_analyzer.analyze_image(image_data)
            
            if not analysis_result:
                logger.warning("No analysis result received")
                return
            
            logger.info(f"Analysis result: {analysis_result[:100]}...")
            
            # Get appropriate emojis based on analysis
            emojis = self.emoji_mapper.get_emojis_for_content(analysis_result)
            
            if not emojis:
                logger.info("No suitable emojis found for this image")
                return
            
            # Add reactions to the message
            for emoji in emojis:
                try:
                    await message.add_reaction(emoji)
                    logger.info(f"Added reaction: {emoji}")
                    # Small delay to avoid rate limits
                    await asyncio.sleep(0.5)
                except discord.HTTPException as e:
                    logger.error(f"Failed to add reaction {emoji}: {e}")
                except Exception as e:
                    logger.error(f"Unexpected error adding reaction {emoji}: {e}")
            
        except Exception as e:
            logger.error(f"Error processing image {attachment.filename}: {e}")
            # Optionally add a generic reaction to indicate processing failed
            try:
                await message.add_reaction("❌")
            except:
                pass

    @commands.command(name='status')
    async def status_command(self, ctx):
        """Check bot status"""
        embed = discord.Embed(
            title="Bot Status",
            color=discord.Color.green(),
            description="Image Recognition Bot is running!"
        )
        embed.add_field(
            name="Monitoring Channel", 
            value=f"<#{self.config.TARGET_CHANNEL_ID}>",
            inline=False
        )
        embed.add_field(
            name="Supported Formats", 
            value="PNG, JPG, JPEG, GIF, WEBP",
            inline=False
        )
        await ctx.send(embed=embed)

    @commands.command(name='test')
    async def test_command(self, ctx):
        """Test command to verify bot is responding"""
        await ctx.send("🤖 Bot is working! Send an image to see magic happen!")

async def main():
    """Main function to run the bot"""
    bot = ImageReactionBot()
    
    try:
        if bot.config.DISCORD_TOKEN:
            await bot.start(bot.config.DISCORD_TOKEN)
        else:
            logger.error("DISCORD_TOKEN is not configured")
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested")
    except Exception as e:
        logger.error(f"Bot encountered an error: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
