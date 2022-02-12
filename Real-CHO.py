import time
import pykorbit
import datetime

key = ""          
secret = ""

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pykorbit.get_ohlc(ticker)
    yesterday = df.iloc[-2]
    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target_price = today_open + (yesterday_high - yesterday_low) * k
    return target_price

def get_balance(ticker):
    """잔고 조회"""
    balance = korbit.get_balances()
    return float(balance[ticker]['available'])

def get_current_price(ticker):
    """현재가 조회"""
    return pykorbit.get_current_price(ticker)

# 로그인
korbit = pykorbit.Korbit(key, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(hours=9)
        end_time = start_time + datetime.timedelta(1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("BTC", 0.2)
            current_price = get_current_price("BTC")
            if target_price < current_price:
                krw = get_balance('krw')
                if krw > 5000:
                    korbit.buy_market_order("BTC", krw*0.9985)
        else:
            btc = get_balance('btc')
            if btc > 0.00009578:
                korbit.sell_market_order("BTC", btc*0.9985)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)