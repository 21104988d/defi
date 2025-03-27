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
    fee = 0.05 / 100  # 0.05% fee
    while True:
        usdt_perp = fetch_btc_usdt_perp("BTCUSDT")
        usdc_perp = fetch_btc_usdt_perp("BTCUSDC")
        usdt_spot = fetch_btc_usdt_spot("BTCUSDT")
        usdc_spot = fetch_btc_usdt_spot("BTCUSDC")
        usdcusdt = fetch_btc_usdt_spot("USDCUSDT")
        
        prices = {
            "USDT Perp": float(usdt_perp),
            "USDC Perp": float(usdc_perp),
            "USDT Spot": float(usdt_spot),
            "USDC Spot": float(usdc_spot),
            "USDCUSDT": float(usdcusdt)
        }

        # Perform triangular arbitrage calculations
        try:
            # Example: Arbitrage between USDT -> USDC -> BTC -> USDT
            usdt_to_usdc = (1 / prices["USDCUSDT"]) * (1 - fee)  # USDT to USDC conversion rate with fee
            usdc_to_btc = (1 / prices["USDC Spot"]) * (1 - fee)  # USDC to BTC conversion rate with fee
            btc_to_usdt = prices["USDT Spot"] * (1 - fee)  # BTC to USDT conversion rate with fee

            # Calculate the final value after completing the triangular arbitrage
            final_value = usdt_to_usdc * usdc_to_btc * btc_to_usdt

            # Check if there's a profitable opportunity
            if final_value > 1:
                profit_percent = (final_value - 1) * 100
                message = f"Triangular Arbitrage Opportunity Detected! Profit: {profit_percent:.2f}%"
                send_telegram_message(message)
            else:
                message = f"No arbitrage opportunity detected. Final Value: {final_value:.6f}%"
                send_telegram_message(message)
        except Exception as e:
            print(f"Error in arbitrage calculation: {e}")

        time.sleep(3)
