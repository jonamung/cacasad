import time
import pykorbit
import datetime

key = ""          
secret = ""

def get_targrt_openmoney(ticker):
    df = pykorbit.get_ohlc(ticker)
    yesterday = df.iloc[-2]
    today_open = yesterday['close']
    return today_open

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
cnt=0
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time1 = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(hours=9)
        start_time2 = datetime.datetime(now.year, now.month, now.day)
        end_time1 = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        end_time2 = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(hours=9) - datetime.timedelta(seconds=10)

        if (start_time1 < now < end_time1) or (start_time2 < now < end_time2):
            targrt_openmoney = get_targrt_openmoney("SAND")
            current_price = get_current_price("SAND")
            if ((targrt_openmoney*0.95) < current_price < (targrt_openmoney*0.98)) and (cnt == 0):
                krw = get_balance('krw')
                if krw > 5000:
                    korbit.buy_market_order("SAND", int(krw*0.9985))
                    cnt=1
            if current_price > (targrt_openmoney*0.98):
                if (targrt_openmoney*0.98) < current_price < (targrt_openmoney*1.02):
                    time.sleep(60)
                    if (targrt_openmoney*0.99) < current_price < (targrt_openmoney*1.02):
                        btc = get_balance('sand')
                        if btc > 0.974:
                            korbit.sell_market_order("SAND", btc*0.9985)
                            cnt=0
        else:
            btc = get_balance('sand')
            if btc > 0.974:
                korbit.sell_market_order("SAND", btc*0.9985)
                cnt=0
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)