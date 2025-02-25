import re
import logging
import asyncio
import MetaTrader5 as mt5
from telethon import TelegramClient, events
from telegram import Bot
import os 
from dotenv import load_dotenv

# Load environment variables from.env file
load_dotenv()

# Logging Configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram API Credentials
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Private Channel ID
BOT_TOKEN= os.getenv("BOT_TOKEN")

# Initialize Telethon Client
client = TelegramClient("my_session", API_ID, API_HASH)

# Initialize Telegram Bot for Notifications
bot = Bot(token=BOT_TOKEN)

# Regex pattern for parsing trade signals
SIGNAL_PATTERN = re.compile(
    r'(?i)(Buy|Sell)\s+Gold\s*@\s*(\d+\.\d+)-(\d+\.\d+).*?SL\s*:\s*(\d+\.\d+).*?TP1\s*:\s*(\d+\.\d+).*?TP2\s*:\s*(\d+\.\d+)',
    re.DOTALL
)

def parse_signal(message: str):
    match = SIGNAL_PATTERN.search(message)
    if match:
        action, entry_low, entry_high, sl, tp1, tp2 = match.groups()
        return {
            'action': action.lower(),
            'symbol': 'XAUUSD',
            'entry': [float(entry_low), float(entry_high)],
            'sl': float(sl),
            'tp1': float(tp1),
            'tp2': float(tp2)
        }
    return None

def execute_trade(data):
    if not mt5.initialize():
        return "❌ MT5 initialization failed."

    symbol = data['symbol']
    if not mt5.symbol_select(symbol, True):
        mt5.shutdown()
        return f"❌ Symbol {symbol} not found or not enabled in Market Watch."

    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        mt5.shutdown()
        return f"❌ Failed to retrieve symbol info for {symbol}."

    symbol_tick = mt5.symbol_info_tick(symbol)
    if not symbol_tick:
        mt5.shutdown()
        return f"❌ No tick data available for {symbol}. Ensure the symbol is active."

    current_price = symbol_tick.ask if data['action'] == 'buy' else symbol_tick.bid
    min_stop_distance = symbol_info.trade_stops_level * symbol_info.point

    if data['action'] == 'buy':
        data['sl'] = min(data['sl'], current_price - min_stop_distance)
        data['tp1'] = max(data['tp1'], current_price + min_stop_distance)
    else:
        data['sl'] = max(data['sl'], current_price + min_stop_distance)
        data['tp1'] = min(data['tp1'], current_price - min_stop_distance)

    lot = 0.1  
    order = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY if data['action'] == "buy" else mt5.ORDER_TYPE_SELL,
        "price": current_price,
        "sl": data['sl'],
        "tp": data['tp1'],
        "deviation": 20,
        "magic": 123456,
        "comment": "Telegram Bot Trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(order)
    mt5.shutdown()

    if result.retcode == mt5.TRADE_RETCODE_DONE:
        return f"✅ Order placed successfully!\nTicket: {result.order}"
    else:
        return f"❌ Order failed. Error: {result.comment}"

async def send_notification(message):
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")

@client.on(events.NewMessage(chats=CHANNEL_ID))
async def handle_new_message(event):
    message_text = event.raw_text
    sender = await event.get_sender()
    sender_name = sender.username or sender.first_name

    logger.info(f"📩 New message from {sender_name}: {message_text}")

    parsed_data = parse_signal(message_text)
    if parsed_data:
        logger.info(f"Trade signal detected: {parsed_data}")
        trade_response = execute_trade(parsed_data)

        response = (
            f"✅ *Trade Signal Executed:*\n"
            f"*Type:* {parsed_data['action'].capitalize()}\n"
            f"*Instrument:* {parsed_data['symbol']}\n"
            f"*Entry Range:* {parsed_data['entry'][0]} - {parsed_data['entry'][1]}\n"
            f"*Stop Loss:* {parsed_data['sl']}\n"
            f"*Take Profit:* {parsed_data['tp1']}, {parsed_data['tp2']}\n\n"
            f"{trade_response}"
        )

        await send_notification(response)
    else:
        logger.info("No valid trade signal detected.")

async def main():
    await client.start()
    print("✅ Telegram bot is now listening for trade signals...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
