import requests
import time

def fetch_btc_usdt_perp(symbol="BTCUSDT"):
    url = "https://fapi.binance.com/fapi/v1/ticker/price"
    params = {"symbol": symbol}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return data.get('price')
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def fetch_btc_usdt_spot(symbol="BTCUSDT"):
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": symbol}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return data.get('price')
    except requests.RequestException as e:
        print(f"Request failed: {e}")

def send_telegram_message(message):
    # Replace 'your_bot_token' and 'your_chat_id' with actual values
    bot_token = "7021088050:AAFfIIqCj94d0nu08j3eMwx2GXEQqOnkJZQ"
    chat_id = "266564928"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to send message: {e}")

if __name__ == "__main__":
    while True:
        usdt_perp = fetch_btc_usdt_perp("BTCUSDT")
        usdc_perp = fetch_btc_usdt_perp("BTCUSDC")
        usdt_spot = fetch_btc_usdt_spot("BTCUSDT")
        usdc_spot = fetch_btc_usdt_spot("BTCUSDC")
        fdusd = fetch_btc_usdt_spot("BTCFDUSD")
        tusd = fetch_btc_usdt_spot("BTCTUSD")
        dai = fetch_btc_usdt_spot("BTCDAI")
        
        prices = {
            "USDT Perp": float(usdt_perp),
            "USDC Perp": float(usdc_perp),
            "USDT Spot": float(usdt_spot),
            "USDC Spot": float(usdc_spot),
            "FDUSD": float(fdusd),
            "TUSD": float(tusd),
            "DAI": float(dai)
        }

        max_diff = 0
        pair = ("", "")
        # Find the biggest price between USDT Perp and USDC Perp
        biggest_perp_price = max(prices["USDT Perp"], prices["USDC Perp"])
        biggest_perp_key = "USDT Perp" if prices["USDT Perp"] > prices["USDC Perp"] else "USDC Perp"

        # Find the biggest difference using the biggest perp price
        for key, price in prices.items():
            if key != biggest_perp_key:
                diff = abs(biggest_perp_price - price)
                if diff > max_diff:
                    max_diff = diff
                    pair = (biggest_perp_key, key)

        average = (prices[pair[0]] + prices[pair[1]]) / 2
        percent = max_diff / average * 100
        #print(f"Greatest Difference: {max_diff} between {pair[0]} and {pair[1]}")
        #print(f"Percent: {percent}%")
        send_telegram_message(f"Alert: Percent difference is {percent}% between {pair[0]} and {pair[1]}")

        time.sleep(3)
