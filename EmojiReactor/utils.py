import logging
import asyncio
from typing import Optional, Tuple
import aiohttp
from PIL import Image
import io

logger = logging.getLogger(__name__)

class ImageUtils:
    """Utility functions for image processing"""
    
    @staticmethod
    def is_valid_image_url(url: str) -> bool:
        """Check if URL appears to be a valid image URL"""
        if not url:
            return False
        
        valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp']
        url_lower = url.lower()
        
        return any(ext in url_lower for ext in valid_extensions)
    
    @staticmethod
    def is_valid_image_size(data: bytes, max_size: int = 10485760) -> bool:
        """Check if image data is within size limits (default 10MB)"""
        return len(data) <= max_size
    
    @staticmethod
    async def download_image(session: aiohttp.ClientSession, url: str, timeout: int = 30) -> Optional[bytes]:
        """
        Download image data from URL
        
        Args:
            session: aiohttp session
            url: Image URL
            timeout: Request timeout in seconds
            
        Returns:
            Image data as bytes, or None if failed
        """
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                if response.status == 200:
                    data = await response.read()
                    logger.debug(f"Downloaded image: {len(data)} bytes from {url}")
                    return data
                else:
                    logger.error(f"Failed to download image: HTTP {response.status}")
                    return None
        except asyncio.TimeoutError:
            logger.error(f"Timeout downloading image from {url}")
            return None
        except Exception as e:
            logger.error(f"Error downloading image from {url}: {e}")
            return None
    
    @staticmethod
    def get_image_info(image_data: bytes) -> Optional[Tuple[str, int, int]]:
        """
        Get basic image information
        
        Args:
            image_data: Image data as bytes
            
        Returns:
            Tuple of (format, width, height) or None if failed
        """
        try:
            with Image.open(io.BytesIO(image_data)) as img:
                return img.format, img.width, img.height
        except Exception as e:
            logger.error(f"Error getting image info: {e}")
            return None
    
    @staticmethod
    def is_animated_gif(image_data: bytes) -> bool:
        """Check if image is an animated GIF"""
        try:
            with Image.open(io.BytesIO(image_data)) as img:
                return img.format == 'GIF' and hasattr(img, 'is_animated') and img.is_animated
        except Exception:
            return False

class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_calls: int, time_window: int):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    async def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        import time
        
        now = time.time()
        
        # Remove old calls outside the time window
        self.calls = [call_time for call_time in self.calls if now - call_time < self.time_window]
        
        # If we're at the limit, wait
        if len(self.calls) >= self.max_calls:
            wait_time = self.time_window - (now - self.calls[0]) + 1
            if wait_time > 0:
                logger.info(f"Rate limit reached, waiting {wait_time:.2f} seconds")
                await asyncio.sleep(wait_time)
        
        # Record this call
        self.calls.append(now)

class MessageUtils:
    """Utility functions for Discord message handling"""
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human-readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100) -> str:
        """Truncate text to specified length with ellipsis"""
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."
    
    @staticmethod
    def extract_urls_from_text(text: str) -> list:
        """Extract URLs from text"""
        import re
        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        return url_pattern.findall(text)

def setup_logging(log_level: str = "INFO", log_file: str = "discord_bot.log"):
    """Setup logging configuration"""
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    
    # Setup file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(console_formatter)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    return root_logger

def validate_environment():
    """Validate that all required environment variables are set"""
    from config import Config
    
    try:
        config = Config()
        config.validate()
        logger.info("Environment validation successful")
        return True
    except ValueError as e:
        logger.error(f"Environment validation failed: {e}")
        return False
