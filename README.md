# Josh Signal Bot

A Telegram signal relay bot — receives trading signals from a Telegram channel and executes trades via MetaTrader 5.

## Features
- Listens to Telegram signal channels
- Parses signal format (symbol, direction, SL, TP)
- Executes trades automatically via MT5

## Requirements
```
pip install telethon MetaTrader5
```

## Configuration
```python
TELEGRAM_API_ID = "your_api_id"
TELEGRAM_API_HASH = "your_api_hash"
CHANNEL = "signal_channel_username"
```

## Usage
```bash
python bot.py
```

## License
MIT
<!-- updated: 2023-02-23-r01 -->
