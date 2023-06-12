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
    api_key: str = "YOUR_BINANCE_API_KEY"
    api_secret: str = "YOUR_BINANCE_API_SECRET"
    client = Client(api_key, api_secret)

    symbol: str = "ETHUSDT"  # Symbol for ETH/USDT futures
    ticker = client.futures_mark_price(symbol=symbol)
    current_price = float(ticker["markPrice"])

    return current_price


# Testing
def test_check_price_change() -> None:
    price_history1: list[float] = [100, 110, 105, 115, 120, 130]  # Change by 30%
    assert check_price_change(price_history1, 10) is True
    assert check_price_change(price_history1, 50) is True
    assert check_price_change(price_history1, 100) is False

    price_history2: list[float] = [100, 110, 105, 115, 120, 130, 135]  # Change by 35%
    assert check_price_change(price_history2, 10) is True
    assert check_price_change(price_history2, 40) is True
    assert check_price_change(price_history2, 50) is False

    price_history3: list[float] = [100, 110, 105, 115, 120, 130, 135, 132]  # Change by 32%
    assert check_price_change(price_history3, 30) is True
    assert check_price_change(price_history3, 35) is True
    assert check_price_change(price_history3, 40) is False

    price_history4: list[float] = [100, 110, 105, 115, 120, 130, 135, 132, 125]  # Change by 25%
    assert check_price_change(price_history4, 20) is True
    assert check_price_change(price_history4, 30) is False
    assert check_price_change(price_history4, 50) is False


def test_run_price_monitor() -> None:
    threshold: float = 1  # Price change threshold - 1%
    run_price_monitor(threshold)


# Run the tests
if __name__ == "__main__":
    test_check_price_change()
    test_run_price_monitor()
