import time
import pykorbit
import datetime

key = "J0xtTdCZkYn3OEkQVSw1pHAAUluoFRPeZOGaMJQfg3JrQZ4tAyvAQtnEj5fSU"          
secret = "3fg0NrS77Ks2yKsPTW4U5fsnJ989UxtH2lmmeEz0zy7GgX5SqNSFcG333yzug"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pykorbit.get_ohlc(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pykorbit.get_ohlc(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balance = korbit.get_balances()
    def get_balance(ticker):
    """잔고 조회"""
    balance = korbit.get_balances()
    return float(balance[ticker]['available'])

def get_current_price(ticker):
    """현재가 조회"""
    return pykorbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
korbit = pykorbit.Korbit(key, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("AMP")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("AMP", 0.2)
            current_price = get_current_price("AMP")
            if target_price < current_price:
                krw = get_balance('krw')
                if krw > 5000:
                    korbit.buy_market_order("AMP", krw*0.9985)
        else:
            btc = get_balance('btc')
            if btc > 5000:
                korbit.sell_market_order("AMP", btc*0.9985)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)