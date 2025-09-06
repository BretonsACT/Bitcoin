import os
import requests
import time
import schedule
from typing import List, Dict, Union

# --- Configuration ---
# It's highly recommended to use environment variables for sensitive data.
# You will need to set these in your operating system or a .env file.
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
RSI_PERIOD = 14
RSI_OVERSOLD_THRESHOLD = 30

def get_bitcoin_price_history() -> List[float]:
    """
    Fetches the last N days of Bitcoin closing prices from the CoinGecko API.
    N is determined by the RSI_PERIOD.
    """
    print("Fetching Bitcoin price history...")
    params = {
        'vs_currency': 'usd',
        'days': RSI_PERIOD + 1, # Fetch a bit more data for calculation stability
        'interval': 'daily'
    }
    try:
        response = requests.get(COINGECKO_API_URL, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        # The API returns timestamps and prices; we only need the prices.
        # [timestamp, price]
        prices = [item[1] for item in data['prices']]
        print(f"Successfully fetched {len(prices)} price points.")
        return prices
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from CoinGecko: {e}")
        return []

def calculate_rsi(prices: List[float], period: int = 14) -> Union[float, None]:
    """
    Calculates the Relative Strength Index (RSI) for a given list of prices.
    RSI is a momentum oscillator that measures the speed and change of price movements.
    """
    if len(prices) < period + 1:
        print("Not enough data to calculate RSI.")
        return None

    print("Calculating RSI...")
    changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    
    gains = [change for change in changes if change > 0]
    losses = [-change for change in changes if change < 0]

    # Calculate initial average gain and loss
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    if avg_loss == 0:
        # Avoid division by zero; RSI is 100 if there are no losses.
        return 100.0

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    print(f"Calculated RSI: {rsi:.2f}")
    return rsi

def send_telegram_message(message: str) -> None:
    """
    Sends a message to a specified Telegram chat using the bot token.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram token or chat ID is not set. Cannot send message.")
        return

    print("Sending Telegram message...")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("Message sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram message: {e}")

def check_and_notify() -> None:
    """
    Main function to check for a buy signal and send a notification.
    """
    print("\n--- Running Daily Bitcoin Check ---")
    
    # Verify that credentials are set before proceeding
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("ERROR: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables must be set.")
        print("Please follow the setup instructions in README.md.")
        # Stop the script if credentials are not found.
        schedule.clear()
        return

    prices = get_bitcoin_price_history()
    if not prices:
        print("Could not retrieve price data. Skipping this check.")
        return

    rsi = calculate_rsi(prices, RSI_PERIOD)
    if rsi is None:
        print("Could not calculate RSI. Skipping this check.")
        return

    if rsi < RSI_OVERSOLD_THRESHOLD:
        message = (
            f"📈 *Bitcoin Buy Signal Detected!* 🚀\n\n"
            f"The daily RSI has dropped to *{rsi:.2f}*, which is below the oversold threshold of {RSI_OVERSOLD_THRESHOLD}.\n\n"
            f"This could indicate a potential buying opportunity.\n\n"
            f"_Disclaimer: This is not financial advice. Always do your own research._"
        )
        send_telegram_message(message)
    else:
        print(f"No buy signal. Current RSI is {rsi:.2f}, which is above the {RSI_OVERSOLD_THRESHOLD} threshold.")
        # Optionally, send a daily status update even if there is no signal
        # send_telegram_message(f"Daily Bitcoin Check: No buy signal. Current RSI is {rsi:.2f}.")

def main():
    """
    Schedules the job and runs it indefinitely.
    """
    print("Starting Bitcoin Buy Signal Bot.")
    
    # Run the check once immediately on startup
    check_and_notify()
    
    # Schedule the check to run every day at a specific time, e.g., 09:00
    schedule.every().day.at("09:00").do(check_and_notify)
    
    print("Scheduler is running. Waiting for the next scheduled check...")
    
    while True:
        schedule.run_pending()
        time.sleep(60) # Check every minute if a scheduled job is due

if __name__ == "__main__":
    main()
