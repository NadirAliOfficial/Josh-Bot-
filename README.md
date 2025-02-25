# Telegram MT5 Trading Bot

## Overview
This project is a Telegram-based trading bot that automatically reads trade signals from a specified Telegram channel and executes trades on MetaTrader 5 (MT5). The bot:
- Listens for new messages in a specified Telegram channel.
- Parses trading signals using regex.
- Places trades on MT5 based on extracted trade parameters.
- Sends trade execution notifications back to Telegram.

## Features
- **Automated Trading Execution**: Reads trade signals and places trades on MT5.
- **Telegram Integration**: Uses `Telethon` to listen for signals and `python-telegram-bot` to send notifications.
- **Logging and Error Handling**: Logs important events for debugging.

## Requirements
### Libraries
Install the necessary dependencies using:
```sh
pip install MetaTrader5 telethon python-telegram-bot asyncio
```

### MetaTrader 5 (MT5) Configuration
- Ensure you have MetaTrader 5 installed and running.
- Add the desired trading symbols to the Market Watch.

### Telegram Credentials
You need the following credentials:
- `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org/)
- `BOT_TOKEN` from [BotFather](https://t.me/BotFather)
- `CHANNEL_ID` of the Telegram channel sending trade signals

## How It Works
1. **Signal Extraction**: The bot uses a regex pattern to extract trade parameters such as Buy/Sell action, entry range, stop loss (SL), and take profits (TP1, TP2) from Telegram messages.
2. **Trade Execution**: If a valid trade signal is detected, the bot:
   - Checks MT5 initialization and symbol availability.
   - Ensures proper stop loss and take profit levels.
   - Places a market order with a predefined lot size (0.1 by default).
3. **Trade Notification**: A confirmation message is sent back to Telegram after execution.

## Configuration
Modify the following variables in the script:
```python
API_ID = 29731527
API_HASH = "your_api_hash"
CHANNEL_ID = -1001735208775
BOT_TOKEN = "your_bot_token"
```
Ensure the channel ID and bot token match your actual Telegram settings.

## Running the Bot
Execute the script:
```sh
python bot.py
```
This will start the Telegram bot, and it will begin monitoring the specified channel for trade signals.

## Example Trade Signal Format
The bot expects signals in the following format:
```
Buy Gold @ 2000.50-2010.00
SL: 1995.00
TP1: 2025.00
TP2: 2050.00
```
It extracts:
- **Action:** Buy
- **Symbol:** XAUUSD (Gold)
- **Entry Range:** 2000.50 - 2010.00
- **Stop Loss:** 1995.00
- **Take Profit 1:** 2025.00
- **Take Profit 2:** 2050.00

## Logging
The bot logs messages and errors:
```sh
2025-02-25 10:00:00 - INFO - 📩 New message received: Buy Gold @ 2000.50-2010.00
2025-02-25 10:00:01 - INFO - ✅ Order placed successfully!
```

## Troubleshooting
- **MT5 Not Initialized**: Ensure that MetaTrader 5 is installed and running.
- **Symbol Not Found**: Check that `XAUUSD` is added to Market Watch in MT5.
- **Telegram API Issues**: Ensure the correct `API_ID`, `API_HASH`, and `BOT_TOKEN`.

## Disclaimer
This bot executes real trades on MT5. Use it at your own risk and test it thoroughly before using it in live trading.

