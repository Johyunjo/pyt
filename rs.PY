# 단일 코인에 대해 RSI 지표 계산하는 코드 
# ticker에 원하는 암호화폐, interval에 원하는 분/일/시
# 매 초마다 현재 RSI값 출력

import pyupbit
import pandas
import datetime
import time

access = "Jvyu0D1AMoOM7KQau9JOeJNQ0kM2CHj9wHYtxYus"
secret = "1Bp2MIMhd4eFI1ReUSGo80pw04UgN4G5Fb50xXWj"

# 로그인
upbit = pyupbit.Upbit(access, secret)
print(upbit.get_balances())
print("autotrade start")

# RSI 계산
def rsi(ohlc: pandas.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0

    AU = ups.ewm(com = period-1, min_periods = period).mean()
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")
time.sleep(0.5) 


# 이용할 코인 리스트
coinlist = ["KRW-BCHA", "KRW-BTC", "KRW-POLY", "KRW-ETH", "KRW-MTL", "KRW-XRP", "KRW-ETC", "KRW-ADA", "KRW-DOT", "KRW-DOGE", "KRW-ELF", "KRW-GLM", "KRW-BTG", "KRW-BTT", "KRW-HIVE"] # Coin ticker 추가
lower27 = []
higher73 = []

# initiate
for i in range(len(coinlist)):
    lower27.append(False)
    higher73.append(False)

# 시장가 매수 함수
def buy(coin):
    money = upbit.get_balance("KRW")
    if money < 15000 :
        res = upbit.buy_market_order(coin, money-10)
    elif money < 50000 :
        res = upbit.buy_market_order(coin, 10000)
    elif money < 100000 :
        res = upbit.buy_market_order(coin, 12000)
    else :
        res = upbit.buy_market_order(coin, money*0.1)

    print(res)
    return

# 시장가 매도 함수
def sell(coin):
    amount = upbit.get_balance(coin)
    cur_price = pyupbit.get_current_price(coin)
    total = amount * cur_price
    prev = upbit.get_balance("KRW")

    if total < 15000 :
        res = upbit.sell_market_order(coin, amount)
    elif total < 30000 :
        res = upbit.sell_market_order(coin, amount*0.5)
    elif total < 50000 :
        res = upbit.sell_market_order(coin, amount*0.35)
    elif total < 100000 :
        res = upbit.sell_market_order(coin, amount*0.2)        
    else :
        res = upbit.sell_market_order(coin, amount*0.15)
    
    post = upbit.get_balance("KRW")

    return


#매매
while(True): 
    for i in range(len(coinlist)): 
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3") 
        now_rsi = rsi(data, 14).iloc[-1] 
        print("코인명: ", coinlist[i]) 
        print("현재시간: ", datetime.datetime.now()) 
        print("RSI :", now_rsi) 
        print() 


    for i in range(len(coinlist)):
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3")
        now_rsi = rsi(data, 14).iloc[-1]
        if now_rsi <= 27 and lower27[i] == False: 
            lower27[i] = True
            print("코인명: ", coinlist[i])
            buy(coinlist[i])

        elif now_rsi >= 73 and higher73[i] == False:
            print("코인명: ", coinlist[i])
            sell(coinlist[i])
            higher73[i] = True

        elif now_rsi >= 45 and now_rsi <= 55:
            lower27[i] = False
            higher73[i] = False
    time.sleep(0.5)