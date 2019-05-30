# общие библиотеки
import datetime
import sys
import sqlite3 as mDB

# мои библиотеки
import bFunc




# исходные данные ----------------



# имя файла БД
sDBname = 'porfolio.db'

# проверка на наличие БД и ее создание в случае отсутствия
try:
    sDBuri = f'file:{pathname2url(sDBname)}?mode=rw'
    dbOne = mDB.connect (sDBuri, uri=True)
    cDbOne = dbOne.cursor()
except mDB.OperationalError:
    dbOne =mDB.connect(sDBname)
    cDbOne = dbOne.cursor()
    # Create table
    cDbOne.execute('''CREATE TABLE rating
                    (datestamp text, 
                    ticker text,
                    prof real,
                    deal real,
                    buy real,
                    sell real)''')

    cDbOne.execute('''CREATE TABLE pair24h
                    (datestamp text, 
                    pair text,
                    baseAsset text,
                    volume real )''')

    # Insert a row of data
    dbOne.commit()





print(f'Запускаем анализ всех пар по валюте {sBase}. Выводы в estimation .txt .db  \n')


# будем писать в файл

# sys.stdout = open('estimation.txt','wt',encoding='utf-8')


# подключаемся к бирже
bot = Binance(
    API_KEY='D7...Ejj',
    API_SECRET='gwQ...u3A'
)



#  интересующие пары 
lPairs = []


# данные по торгуемым парам

lExchangeInfo = bot.exchangeInfo()
iCountPair = 0
lTicker = []
for lEI in lExchangeInfo['symbols']:
    # print(lEI)
    # print(lEI['status'])
    if (lEI['status'] == 'TRADING') and ((lEI['baseAsset']==sBase) or (lEI['quoteAsset']==sBase)) :
        lTicker24h = bot.ticker24hr(symbol=lEI['symbol'])
        if lEI['baseAsset']==sBase:
            lPairs.append([lEI['symbol'], lEI['baseAsset'], lEI['quoteAsset'], float(lTicker24h['volume']) ])    
        else:
            lPairs.append([lEI['symbol'], lEI['baseAsset'], lEI['quoteAsset'], float(lTicker24h['quoteVolume']) ])    
lPairs.sort(key=lambda ii: ii[3],reverse=True)



for lPair in lPairs:
    iCountPair +=1
    print(f'№ {iCountPair:03d} Пара: {lPair[0]:10s} Оборот за 24h: {lPair[3]: 15.2f} {sBase}')    
    cDbOne.execute(f"INSERT INTO pair24h VALUES ('2019/02/01','{lPair[0]}','{sBase}','{lPair[3]}')")

    #  данные с биржи по свечам
    slKLines = bot.klines(
        symbol=lPair[0],
        interval=sInterval,
        limit=iLimit)
    # вычисляем !!!
    bFunc.estimationPair(slKLines,lPair[0],iLimit,sInterval,iCountPrint,iCountTrade,cDbOne)

dbOne.commit()
dbOne.close()