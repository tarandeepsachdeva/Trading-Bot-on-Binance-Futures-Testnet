# Simplified Binance Futures Trading Bot

A structured Python command-line application designed to place orders on the Binance Futures Testnet (USDT-M) platform. This project features a clean, modular layout with separate client, validation, and command layers, along with structured logging and error handling.

## Project Structure
This application follows the recommended project directory layout:
```text
TRADING_BOT/
│
├── Bot/
│   ├── __init__.py
│   ├── client.py          # Binance client wrapper
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Structured logging wrapper
│
├── cli.py                 # CLI entry point
├── bot.log                # Generated application logs
└── requirements.txt       # Project dependencies

## Installation & Setup

1. **Clone or Extract the folder** and navigate to the root directory:
   ```bash
   cd trading_bot
Install required dependencies:
Bash
pip install -r requirements.txt
Configure API Credentials:
Open cli.py and replace the placeholder API_KEY and API_SECRET strings with your official Binance Futures Testnet credentials.
Execution Guide
1. Execute a MARKET Order Example
Bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.005
2. Execute a LIMIT Order Example
Bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.005 --price 60000

---

### Step 8: Running Your Bot & Generating the Deliverables
The hiring team wants you to submit the **`bot.log`** file showcasing at least one successful MARKET order and one successful LIMIT order [cite: 57-61].

1. Open your computer terminal inside your `trading_bot` directory.
2. Execute this command to test a **Market Buy** order:
   ```bash
   python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002