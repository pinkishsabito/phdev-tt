import time
from binance.client import Client


def check_price_change(price_history: list[float], threshold: float) -> bool:
    if len(price_history) < 60:
        return False

    start_price = price_history[0]
    current_price = price_history[-1]
    percent_change = ((current_price - start_price) / start_price) * 100

    return abs(percent_change) >= threshold


def run_price_monitor(threshold: float) -> None:
    price_history: list[float] = []

    while True:
        current_price = get_current_price()
        price_history.append(current_price)

        if len(price_history) > 60:
            price_history = price_history[1:]

        if check_price_change(price_history, threshold):
            print(f"Price changed by {threshold}% in the last 60 minutes!")

        time.sleep(60)


def get_current_price() -> float:
    api_key: str = 'YOUR_BINANCE_API_KEY'
    api_secret: str = 'YOUR_BINANCE_API_SECRET'
    client = Client(api_key, api_secret)

    symbol: str = 'ETHUSDT'  # Symbol for ETH/USDT futures
    ticker = client.futures_mark_price(symbol=symbol)
    current_price = float(ticker['markPrice'])

    return current_price
