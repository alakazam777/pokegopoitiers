import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the Discord bot"""
    
    def __init__(self):
        # Discord Configuration
        self.DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
        if not self.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN environment variable is required")
        
        self.TARGET_CHANNEL_ID = os.getenv("TARGET_CHANNEL_ID")
        if not self.TARGET_CHANNEL_ID:
            raise ValueError("TARGET_CHANNEL_ID environment variable is required")
        
        # OpenAI Configuration
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not self.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Bot Configuration
        self.MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", "10485760"))  # 10MB default
        self.ANALYSIS_TIMEOUT = int(os.getenv("ANALYSIS_TIMEOUT", "30"))  # 30 seconds
        self.MAX_EMOJIS_PER_IMAGE = int(os.getenv("MAX_EMOJIS_PER_IMAGE", "3"))
        
        # Logging Configuration
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
        
    def validate(self):
        """Validate all required configuration values"""
        required_vars = [
            "DISCORD_TOKEN",
            "TARGET_CHANNEL_ID", 
            "OPENAI_API_KEY"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(self, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
