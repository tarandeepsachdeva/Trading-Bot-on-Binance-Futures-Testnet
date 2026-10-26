# Binance Futures Trading Bot

A Python-based trading bot for Binance Futures Testnet with both CLI and GUI interfaces. This project demonstrates API integration, order placement, and account management for cryptocurrency futures trading.

## Features

- **CLI Interface**: Command-line tool for placing orders
- **GUI Interface**: Modern dark-themed tkinter interface with tabs for trading and assets
- **Order Types**: Support for MARKET and LIMIT orders
- **Asset Management**: View all account assets with detailed balance information
- **Real-time Data**: Live connection to Binance Futures Testnet
- **Input Validation**: Comprehensive validation for all order parameters

## Project Structure

```
Trading_bot/
│
├── Bot/
│   ├── __init__.py
│   ├── client.py          # Binance client wrapper
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Structured logging
│
├── cli.py                 # CLI entry point
├── gui.py                 # GUI entry point
├── requirements.txt       # Project dependencies
└── README.md             # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tarandeepsachdeva/Trading-Bot-on-Binance-Futures-Testnet.git
   cd Trading-Bot-on-Binance-Futures-Testnet
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Credentials**
   
   Open `cli.py` and `gui.py`, then replace the placeholder API_KEY and API_SECRET with your Binance Futures Testnet credentials:
   ```python
   API_KEY = "your_api_key_here"
   API_SECRET = "your_api_secret_here"
   ```

## Usage

### CLI Interface

**Place a MARKET Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**Place a LIMIT Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 60000
```

### GUI Interface

Launch the graphical interface:
```bash
python gui.py
```

**GUI Features:**
- **Trading Tab**: Place orders with an intuitive form
- **Assets Tab**: View account balance and all assets
- **Real-time Updates**: Refresh assets button to get latest account data
- **Order Response**: Detailed feedback for each order

## GUI Screenshots

The GUI features:
- Dark theme matching Binance's aesthetic
- Color-coded BUY (green) and SELL (red) options
- Tabbed interface for Trading and Assets
- Comprehensive asset display matching Binance's format

## Order Parameters

| Parameter | Description | Required | Values |
|-----------|-------------|----------|--------|
| `--symbol` | Trading pair symbol | Yes | e.g., BTCUSDT, ETHUSDT |
| `--side` | Order direction | Yes | BUY, SELL |
| `--type` | Order type | Yes | MARKET, LIMIT |
| `--quantity` | Order quantity | Yes | Positive number |
| `--price` | Target price | No (for LIMIT) | Positive number |

## Account Information

The Assets tab displays:
- Total Margin Balance
- Total Wallet Balance
- Unrealized PNL
- Individual asset details (Wallet Balance, Unrealized PNL, Margin Balance, Available for Transfer)

## Security Notes

⚠️ **Important**: This project uses Binance Testnet for development. Never use your mainnet API keys in testnet environments.

- API keys are currently stored in the source files for educational purposes
- For production use, implement environment variables or secure credential management
- Never commit real API keys to public repositories

## Technical Details

- **Python Version**: 3.x
- **Library**: python-binance
- **API**: Binance Futures Testnet
- **GUI Framework**: tkinter

## Error Handling

The bot includes comprehensive error handling for:
- Invalid API credentials
- Network connection issues
- Invalid input parameters
- Insufficient balance
- Binance API errors

## Logging

All operations are logged with structured logging for debugging and audit purposes.

## License

This project is for educational purposes only. Use at your own risk when trading with real funds.

## Contributing

Feel free to submit issues and enhancement requests!

## Disclaimer

This software is provided as-is for educational purposes. Cryptocurrency trading involves significant risk. The authors are not responsible for any financial losses incurred while using this software.
