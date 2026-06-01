
import logging

logger = logging.getLogger(__name__)

def place_futures_order(client, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    """
    Sends the validated order request to Binance Futures Testnet.
    """
    symbol = symbol.upper()
    side = side.upper()
    order_type = order_type.upper()

    try:
        logger.info(f"Sending order request: {side} {quantity} {symbol} ({order_type})")
        
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity
        }
        
        
        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"  

        
        response = client.futures_create_order(**params)
        
        logger.info(f"Order successfully placed! OrderID: {response.get('orderId')}")
        return response

    except Exception as e:
        logger.error(f"Binance API Error occurred while placing order: {str(e)}")
        raise e