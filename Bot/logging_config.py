
import logging
import os

def setup_logging():
    """Sets up standard application-wide logging to a file."""
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler("bot.log"),
            logging.StreamHandler() 
        ]
    )
    return logging.getLogger(__name__)