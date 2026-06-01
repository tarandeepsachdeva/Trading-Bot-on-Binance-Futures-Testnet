
import argparse
import sys
from Bot.logging_config import setup_logging
from Bot.client import get_binance_client
from Bot.validators import validate_inputs
from Bot.orders import place_futures_order


API_KEY = "7ZXwpbQanNNqHBdzNcpZbKAcDuVrrlak6aword5wl89sMhBibZQp4Lac0xCDHIyd"
API_SECRET = "jygIvBiV1HoiDjW9RUDKcHc1ZifktieuDafcABMUpa3z4LoXobuZ6XUfIfGudQAp"

def main():
    
    logger = setup_logging()
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot CLI")
    parser.add_argument("--symbol", type=str, required=True, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, required=True, help="BUY or SELL")
    parser.add_argument("--type", type=str, required=True, help="MARKET or LIMIT")
    parser.add_argument("--quantity", type=float, required=True, help="Order quantity amount")
    parser.add_argument("--price", type=float, default=None, help="Target price (Required only for LIMIT orders)")
    
    args = parser.parse_args()
    
    
    try:
        validate_inputs(args.symbol, args.side, args.type, args.quantity, args.price)
    except ValueError as e:
        logger.error(f"Validation Error: {str(e)}")
        print(f"\n Validation Failure: {str(e)}")
        sys.exit(1)
        
    
    try:
        client = get_binance_client(API_KEY, API_SECRET)
    except Exception as e:
        print(f"\n Connection Failure: Check your internet or API credentials.")
        sys.exit(1)
        
    
    print("\n==============================")
    print(" ORDER REQUEST SUMMARY")
    print("==============================")
    print(f"Symbol:   {args.symbol.upper()}")
    print(f"Side:     {args.side.upper()}")
    print(f"Type:     {args.type.upper()}")
    print(f"Quantity: {args.quantity}")
    if args.price:
        print(f"Price:    {args.price}")
    print("==============================\n")
    
    
    try:
        response = place_futures_order(client, args.symbol, args.side, args.type, args.quantity, args.price)
        
        
        print("SUCCESS: Order processed cleanly by server!")
        print("\n==============================")
        print("ORDER RESPONSE DETAILS")
        print("==============================")
        print(f"OrderID:      {response.get('orderId')}")
        print(f"Status:       {response.get('status')}")
        print(f"Executed Qty: {response.get('executedQty')}")
        print(f"Avg Price:    {response.get('avgPrice', 'N/A')}")
        print("==============================\n")
        
    except Exception as e:
        print(f"\n EXECUTION FAILURE: Binance rejected the transaction.")
        print(f"Reason: {str(e)}")

if __name__ == "__main__":
    main()