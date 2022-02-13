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
        start_time1 = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(hours=9)
        start_time2 = datetime.datetime(now.year, now.month, now.day)
        end_time1 = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        end_time2 = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(hours=9) - datetime.timedelta(seconds=10)

        if (start_time1 < now < end_time1) or (start_time2 < now < end_time2):
            target_price = get_target_price("SAND", 0.2)
            current_price = get_current_price("SAND")
            if target_price < current_price:
                krw = get_balance('krw')
                if krw > 5000:
                    korbit.buy_market_order("SAND", krw*0.9985)
        else:
            btc = get_balance('sand')
            if btc > 0.974:
                korbit.sell_market_order("SAND", btc*0.9985)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)