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

def rsi(ohlc: pandas.DataFrame, period: int = 14): 
    delta = ohlc["close"].diff() 
    ups, downs = delta.copy(), delta.copy() 
    ups[ups < 0] = 0 
    downs[downs > 0] = 0 
    
    AU = ups.ewm(com = period-1, min_periods = period).mean() 
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean() 
    RS = AU/AD 
    
    return pandas.Series(100 - (100/(1 + RS)), name = "RSI") 

coinlist = ["KRW-BCHA", "KRW-BTC", "KRW-SAND", "KRW-ETH", "KRW-MTL", "KRW-XRP", "KRW-ETC", "KRW-ADA", "KRW-DOT", "KRW-DOGE"] 
lower28 = []
higher70 = [] 

# initiate lower28은 이전에 28 이하를 찍었는지, higher70은 70 이상을 찍었는지를 담고 있는 리스트이다. 
for i in range(len(coinlist)): 
    lower28.append(False) 
    higher70.append(False)

while(True): 
    for i in range(len(coinlist)): 
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3") 
        now_rsi = rsi(data, 14).iloc[-1] 
        print("코인명: ", coinlist[i]) 
        print("현재시간: ", datetime.datetime.now()) 
        print("RSI :", now_rsi) 
        print() 
        time.sleep(0.5)

# 시장가 매수 함수 
    def buy(coin): 
        money = upbit.get_balance("KRW") 
        if money < 15000 : 
            res = upbit.buy_market_order(coin, money-10) 
        elif money < 50000: 
            res = upbit.buy_market_order(coin, 10000) 
        elif money < 100000 : 
            res = upbit.buy_market_order(coin, 12000) 
        else : res = upbit.buy_market_order(coin, money*0.1) 
        return 
        
        # 시장가 매도 함수 
    def sell(coin): 
        amount = upbit.get_balance(coin) 
        cur_price = pyupbit.get_current_price(coin) 
        total = amount * cur_price 
        prev = upbit.get_balance("KRW")

        if total < 15000 : 
            res = upbit.sell_market_order(coin, amount) 
        elif total < 30000: 
            res = upbit.sell_market_order(coin, amount*0.5) 
        elif total < 50000: 
            res = upbit.sell_market_order(coin, amount*0.35)
        elif total < 100000 : 
            res = upbit.sell_market_order(coin, amount*0.2)

        else : res = upbit.sell_market_order(coin, amount*0.15) 

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

#RSI가 28 이하가 된다면 lower28을 true로 바꿔준다. 
        if now_rsi <= 28 : 
           lower28[i] = True 

#만약 lower28[i]가 true이고, 현재 RSI값이 33 이상이라면, 매수 조건을 만족한 경우이므로 매수를 진행한다. 
        elif now_rsi >= 33 and lower28[i] == True: 
            buy(coinlist[i]) 
            lower28[i] = False 
        elif now_rsi <= 45 : 
            higher70[i] = False 

#RSI값이 70 이상이 되었을 때 한번 매도를 한다면, 이후에는 RSI가 적어도 60까지는 내려갔다가 다시 올라오는 경우에 매도            
        elif now_rsi >= 70 and higher70[i] == False: 
           sell(coinlist[i]) 
           higher70[i] = True 
        elif now_rsi <= 60 : 
            higher70[i] = False 
        time.sleep(0.5)





