
import logging

logger = logging.getLogger(__name__)

def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    """
    Validates user inputs before sending them to the Binance API.
    Raises ValueError if inputs are invalid.
    """
    
    if not symbol or not symbol.isalnum():
        raise ValueError("Invalid symbol. Example: BTCUSDT")

    
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError("Side must be either 'BUY' or 'SELL'.")

    
    if order_type.upper() not in ["MARKET", "LIMIT"]:
        raise ValueError("Order type must be either 'MARKET' or 'LIMIT'.")

    
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    
    if order_type.upper() == "LIMIT" and (price is None or price <= 0):
        raise ValueError("Price is required and must be greater than 0 for LIMIT orders.")
        
    logger.info("All inputs successfully validated.")
    return True