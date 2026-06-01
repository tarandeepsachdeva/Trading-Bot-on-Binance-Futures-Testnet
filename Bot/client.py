
from binance.client import Client
import logging

logger = logging.getLogger(__name__)

def get_binance_client(api_key: str, api_secret: str):
    """Initializes and returns the Binance Futures Testnet Client."""
    if not api_key or not api_secret:
        logger.error("API Key or Secret Key is missing!")
        raise ValueError("API credentials cannot be empty.")
    
    try:
        
        client = Client(api_key, api_secret, testnet=True)
        logger.info("Successfully connected to Binance Futures Testnet Client.")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to Binance API: {str(e)}")
        raise e