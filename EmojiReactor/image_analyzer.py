import base64
import json
import logging
from openai import OpenAI
from config import Config
import asyncio
from typing import Optional

logger = logging.getLogger(__name__)

class ImageAnalyzer:
    """Handles image analysis using OpenAI Vision API"""
    
    def __init__(self):
        self.config = Config()
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.client = OpenAI(api_key=self.config.OPENAI_API_KEY)
        self.model = "gpt-4o"
    
    async def analyze_image(self, image_data: bytes) -> Optional[str]:
        """
        Analyze an image using OpenAI Vision API
        
        Args:
            image_data: Image data as bytes
            
        Returns:
            Analysis result as string, or None if analysis failed
        """
        try:
            # Convert image to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Create the analysis prompt
            system_prompt = """You are an expert image analyzer for a Discord bot that adds emoji reactions.
            Analyze the image and provide a detailed description focusing on:
            1. Main subjects/objects in the image
            2. Activities or actions taking place
            3. Emotions or mood conveyed
            4. Setting or environment
            5. Colors and visual elements
            6. Any text visible in the image
            
            Be specific and detailed to help determine appropriate emoji reactions.
            Focus on concrete, identifiable elements rather than abstract interpretations."""
            
            user_prompt = "Analyze this image in detail and describe all key elements you can identify."
            
            # Make API call in a thread to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                self._make_vision_request,
                base64_image,
                system_prompt,
                user_prompt
            )
            
            if response and response.choices:
                analysis = response.choices[0].message.content
                logger.info("Successfully analyzed image")
                return analysis
            else:
                logger.error("No response from OpenAI Vision API")
                return None
                
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return None
    
    def _make_vision_request(self, base64_image: str, system_prompt: str, user_prompt: str):
        """Make the actual API request (runs in thread)"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response
        except Exception as e:
            logger.error(f"OpenAI API request failed: {e}")
            return None
    
    async def get_emoji_suggestions(self, analysis: str) -> Optional[list]:
        """
        Get emoji suggestions based on image analysis
        
        Args:
            analysis: The image analysis text
            
        Returns:
            List of suggested emojis, or None if failed
        """
        try:
            prompt = f"""Based on this image analysis, suggest 3-5 appropriate Discord emojis that would be good reactions.
            
Image Analysis: {analysis}

Respond with a JSON object containing an array of emoji suggestions with explanations:
{{
    "emojis": [
        {{"emoji": "😍", "reason": "for beautiful/attractive content"}},
        {{"emoji": "🔥", "reason": "for impressive/amazing content"}},
        {{"emoji": "👏", "reason": "for appreciative reactions"}}
    ]
}}

Choose emojis that are commonly available on Discord and match the content well."""
            
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                self._make_emoji_request,
                prompt
            )
            
            if response and response.choices:
                content = response.choices[0].message.content
                try:
                    result = json.loads(content)
                    return [item["emoji"] for item in result.get("emojis", [])]
                except json.JSONDecodeError:
                    logger.error("Failed to parse emoji suggestions JSON")
                    return None
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting emoji suggestions: {e}")
            return None
    
    def _make_emoji_request(self, prompt: str):
        """Make emoji suggestion API request (runs in thread)"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300,
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            return response
        except Exception as e:
            logger.error(f"OpenAI emoji suggestion request failed: {e}")
            return None
