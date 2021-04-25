import time
import pyupbit
import datetime

access = "YavQpFdQ7G30UHmKnmNVCYtZxrkZyhX2xVmb5w5n"
secret = "5vokVHwQOKkpK4d8SEGNusxoOC2XsESL1EijUIox"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now() #9시
        start_time = get_start_time("KRW-EOS")
        end_time = start_time + datetime.timedelta(days=1) #9시 +1일

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-EOS", 0.5)
            current_price = get_current_price("KRW-EOS")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-EOS", krw*0.9995*0.2) #잔고의 20%만 매수
        else:
            btc = get_balance("EOS")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-EOS", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
