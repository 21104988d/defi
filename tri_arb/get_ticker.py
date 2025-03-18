import ccxt

pionex = ccxt.pionex({'enableRateLimit': True})

def get_tickers():
    tickers = pionex.fetch_tickers()
    # 過濾出BTC/USDT, ETH/BTC, ETH/USDT等相關交易對
    return {symbol: ticker['last'] for symbol, ticker in tickers.items()}

def find_arb_opportunities(tickers):
    opportunities = []
    pairs = list(tickers.keys())
    # 生成所有可能的三元組組合
    for base in pairs:
        for intermediate in pairs:
            for quote in pairs:
                if base != intermediate and intermediate != quote:
                    # Skip the specified pairs
                    if (f"{base}/{intermediate}" in ["BTC/USDT", "ETH/USDT", "ETH/BTC"] or
                        f"{intermediate}/{quote}" in ["BTC/USDT", "ETH/USDT", "ETH/BTC"] or
                        f"{base}/{quote}" in ["BTC/USDT", "ETH/USDT", "ETH/BTC"]):
                        continue
                    rate1 = tickers[f"{base}/{intermediate}"]
                    rate2 = tickers[f"{intermediate}/{quote}"]
                    rate3 = 1 / tickers[f"{base}/{quote}"]
                    if rate1 * rate2 * rate3 > 1.003:  # 需覆蓋成本
                        opportunities.append((base, intermediate, quote))
    return opportunities