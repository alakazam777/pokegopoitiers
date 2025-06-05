import re
import logging
from typing import List, Set
import random

logger = logging.getLogger(__name__)

class EmojiMapper:
    """Maps image analysis content to appropriate emoji reactions"""
    
    def __init__(self):
        # Define emoji mappings based on content keywords
        self.emoji_mappings = {
            # Animals
            'cat': ['🐱', '😸', '😻', '🙀'],
            'dog': ['🐶', '🐕', '🦮', '🐕‍🦺'],
            'bird': ['🐦', '🦅', '🦆', '🐧'],
            'fish': ['🐟', '🐠', '🐡', '🦈'],
            'horse': ['🐴', '🐎', '🦄'],
            'cow': ['🐄', '🐮'],
            'pig': ['🐷', '🐖'],
            'monkey': ['🐵', '🐒'],
            'lion': ['🦁'],
            'tiger': ['🐯'],
            'bear': ['🐻', '🧸'],
            'panda': ['🐼'],
            'rabbit': ['🐰', '🐇'],
            'fox': ['🦊'],
            'wolf': ['🐺'],
            'frog': ['🐸'],
            'turtle': ['🐢'],
            'snake': ['🐍'],
            'dragon': ['🐉', '🐲'],
            'unicorn': ['🦄'],
            
            # Food & Drink
            'pizza': ['🍕'],
            'burger': ['🍔'],
            'food': ['🍽️', '😋', '🤤'],
            'cake': ['🎂', '🧁'],
            'coffee': ['☕', '☕️'],
            'beer': ['🍺', '🍻'],
            'wine': ['🍷', '🍾'],
            'ice cream': ['🍦', '🍨'],
            'fruit': ['🍎', '🍊', '🍌', '🍇'],
            'apple': ['🍎'],
            'banana': ['🍌'],
            'orange': ['🍊'],
            'strawberry': ['🍓'],
            'bread': ['🍞', '🥖'],
            'meat': ['🥩', '🍖'],
            'chicken': ['🍗'],
            'egg': ['🥚', '🍳'],
            'pasta': ['🍝'],
            'soup': ['🍲'],
            'salad': ['🥗'],
            
            # Nature & Weather
            'sun': ['☀️', '🌞'],
            'moon': ['🌙', '🌛', '🌜'],
            'star': ['⭐', '🌟', '✨'],
            'cloud': ['☁️', '⛅'],
            'rain': ['🌧️', '☔', '💧'],
            'snow': ['❄️', '⛄', '🌨️'],
            'rainbow': ['🌈'],
            'flower': ['🌸', '🌺', '🌻', '🌷', '🌹'],
            'tree': ['🌳', '🌲', '🎋'],
            'mountain': ['⛰️', '🏔️'],
            'ocean': ['🌊', '🏖️'],
            'beach': ['🏖️', '🌊'],
            'fire': ['🔥', '🚒'],
            'water': ['💧', '🌊'],
            'earth': ['🌍', '🌎', '🌏'],
            
            # Activities & Sports
            'sport': ['⚽', '🏀', '🏈', '⚾', '🎾'],
            'football': ['⚽', '🏈'],
            'basketball': ['🏀'],
            'tennis': ['🎾'],
            'swimming': ['🏊‍♂️', '🏊‍♀️', '🌊'],
            'running': ['🏃‍♂️', '🏃‍♀️', '💨'],
            'cycling': ['🚴‍♂️', '🚴‍♀️', '🚲'],
            'dancing': ['💃', '🕺'],
            'music': ['🎵', '🎶', '🎤', '🎸', '🎹'],
            'gaming': ['🎮', '🕹️'],
            'reading': ['📚', '📖'],
            'cooking': ['👨‍🍳', '👩‍🍳', '🍳'],
            'art': ['🎨', '🖼️', '✏️'],
            'photography': ['📸', '📷'],
            
            # Emotions & Expressions
            'happy': ['😊', '😄', '😁', '🙂', '😀'],
            'sad': ['😢', '😭', '☹️', '😞'],
            'angry': ['😠', '😡', '🤬'],
            'love': ['❤️', '💕', '💖', '💗', '💙', '💚', '💛', '🧡', '💜'],
            'heart': ['❤️', '💕', '💖', '💗'],
            'laugh': ['😂', '🤣', '😆'],
            'surprise': ['😮', '😲', '🤯'],
            'excited': ['🤩', '😍', '🥳'],
            'cool': ['😎', '🆒'],
            'amazing': ['🤩', '😍', '🔥', '💯'],
            'beautiful': ['😍', '🤩', '✨', '💖'],
            'cute': ['🥰', '😍', '🥺', '💕'],
            
            # Transportation
            'car': ['🚗', '🚙', '🏎️'],
            'truck': ['🚚', '🚛'],
            'plane': ['✈️', '🛩️'],
            'train': ['🚂', '🚆', '🚇'],
            'bus': ['🚌', '🚍'],
            'bike': ['🚴‍♂️', '🚴‍♀️', '🚲'],
            'motorcycle': ['🏍️'],
            'boat': ['⛵', '🚤', '🛥️'],
            'rocket': ['🚀'],
            
            # Technology
            'computer': ['💻', '🖥️'],
            'phone': ['📱', '☎️'],
            'camera': ['📸', '📷'],
            'robot': ['🤖'],
            'tech': ['⚡', '🔧', '⚙️'],
            
            # Objects & Items  
            'book': ['📚', '📖'],
            'gift': ['🎁'],
            'money': ['💰', '💵', '💸'],
            'home': ['🏠', '🏡'],
            'building': ['🏢', '🏬', '🏭'],
            'school': ['🏫', '🎓'],
            'hospital': ['🏥', '⚕️'],
            'church': ['⛪', '🕌'],
            'flag': ['🏴', '🏳️'],
            'crown': ['👑'],
            'diamond': ['💎'],
            'key': ['🔑', '🗝️'],
            'lock': ['🔒', '🔓'],
            'tool': ['🔧', '🔨', '⚙️'],
            
            # Colors
            'red': ['❤️', '🔴', '🌹'],
            'blue': ['💙', '🔵', '🌀'],
            'green': ['💚', '🟢', '🌿'],
            'yellow': ['💛', '🟡', '⭐'],
            'purple': ['💜', '🟣', '🔮'],
            'orange': ['🧡', '🟠', '🍊'],
            'black': ['🖤', '⚫'],
            'white': ['🤍', '⚪'],
            'pink': ['🩷', '🌸', '🌺'],
            
            # Time & Events
            'birthday': ['🎂', '🥳', '🎉'],
            'party': ['🎉', '🥳', '🍾'],
            'celebration': ['🎉', '🥳', '🎊'],
            'wedding': ['💒', '👰', '🤵', '💍'],
            'christmas': ['🎄', '🎅', '🤶', '⛄'],
            'halloween': ['🎃', '👻', '🦇'],
            'new year': ['🎊', '🥂', '🎆'],
            
            # Professions
            'doctor': ['👨‍⚕️', '👩‍⚕️', '⚕️'],
            'teacher': ['👨‍🏫', '👩‍🏫', '📚'],
            'police': ['👮‍♂️', '👮‍♀️', '🚔'],
            'firefighter': ['👨‍🚒', '👩‍🚒', '🚒'],
            'chef': ['👨‍🍳', '👩‍🍳', '🍳'],
            'farmer': ['👨‍🌾', '👩‍🌾', '🚜'],
        }
        
        # Generic positive reactions
        self.positive_reactions = ['👍', '👏', '🔥', '💯', '✨', '⭐', '😍']
        
        # Generic neutral reactions  
        self.neutral_reactions = ['👀', '🤔', '😮', '🙂']
        
        # Fallback emojis for when no specific match is found
        self.fallback_emojis = ['👀', '😊', '👍', '✨']

    def get_emojis_for_content(self, analysis_text: str, max_emojis: int = 3) -> List[str]:
        """
        Get appropriate emojis based on image analysis content
        
        Args:
            analysis_text: The image analysis text from OpenAI
            max_emojis: Maximum number of emojis to return
            
        Returns:
            List of emoji strings
        """
        try:
            if not analysis_text:
                return self.fallback_emojis[:max_emojis]
            
            # Convert to lowercase for matching
            text_lower = analysis_text.lower()
            
            # Find matching emojis
            matched_emojis = set()
            
            # Check for keyword matches
            for keyword, emojis in self.emoji_mappings.items():
                if keyword in text_lower:
                    # Add random emoji from the category
                    matched_emojis.add(random.choice(emojis))
                    logger.debug(f"Matched keyword '{keyword}' -> {emojis[0]}")
            
            # Convert to list and limit
            emoji_list = list(matched_emojis)
            
            # If we have matches, return them (up to max_emojis)
            if emoji_list:
                if len(emoji_list) > max_emojis:
                    emoji_list = random.sample(emoji_list, max_emojis)
                return emoji_list
            
            # If no specific matches, use sentiment-based selection
            return self._get_sentiment_emojis(text_lower, max_emojis)
            
        except Exception as e:
            logger.error(f"Error mapping emojis: {e}")
            return self.fallback_emojis[:max_emojis]
    
    def _get_sentiment_emojis(self, text: str, max_emojis: int) -> List[str]:
        """Get emojis based on sentiment analysis of the text"""
        try:
            # Simple sentiment keywords
            positive_words = [
                'beautiful', 'amazing', 'wonderful', 'great', 'awesome', 'fantastic',
                'lovely', 'perfect', 'excellent', 'stunning', 'gorgeous', 'incredible',
                'impressive', 'brilliant', 'magnificent', 'spectacular', 'marvelous',
                'delightful', 'charming', 'elegant', 'graceful', 'vibrant', 'colorful'
            ]
            
            negative_words = [
                'sad', 'terrible', 'awful', 'bad', 'horrible', 'ugly', 'disgusting',
                'disappointing', 'boring', 'dull', 'dark', 'gloomy', 'depressing'
            ]
            
            positive_count = sum(1 for word in positive_words if word in text)
            negative_count = sum(1 for word in negative_words if word in text)
            
            if positive_count > negative_count:
                return random.sample(self.positive_reactions, min(max_emojis, len(self.positive_reactions)))
            elif negative_count > positive_count:
                return ['😔', '😞', '💔'][:max_emojis]
            else:
                return random.sample(self.neutral_reactions, min(max_emojis, len(self.neutral_reactions)))
                
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return self.fallback_emojis[:max_emojis]
    
    def add_custom_mapping(self, keyword: str, emojis: List[str]):
        """Add custom keyword -> emoji mapping"""
        self.emoji_mappings[keyword.lower()] = emojis
        logger.info(f"Added custom mapping: {keyword} -> {emojis}")
    
    def remove_mapping(self, keyword: str):
        """Remove a keyword mapping"""
        if keyword.lower() in self.emoji_mappings:
            del self.emoji_mappings[keyword.lower()]
            logger.info(f"Removed mapping for: {keyword}")
