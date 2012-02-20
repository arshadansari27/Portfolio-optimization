'''
Created on Feb 14, 2012

@author: arshadansari
'''
import pickle, redis

StockGroupKey = "StockGroup:%s:%s"
StockKey = "Stock:%s"
CorrelationKey = "StockCoRelation:%s:%s"


class RedisAccess:

    def __init__(self):
        self.__redis = redis.Redis("localhost")

    def getKeyMatching(self, pattern):
        return self.__redis.keys(pattern)

    def getValue(self, key):
        return self.__redis.get(key)

    def setValue(self, key, value):
        return self.__redis.set(key, value)

    def appendValue(self, key, value):
        return self.__redis.append(key, value)

    def remove(self, key):
        return self.__redis.delete(key)

    def getAll(self, keys):
        self.__redis.mget(keys)

redisAccess = RedisAccess()

def getStock(stock):
    stockString = redisAccess.getValue(StockKey % stock.uid)
    if stockString is not None:
        return pickle.loads(stockString)
    return None


def getAllStocks():
    keys = redisAccess.getKeyMatching(StockKey % '*')
    stockList = []

    for key in keys:
        stock = redisAccess.getValue(key)
        if stock is not None:
            stockList.append(pickle.loads(stock))
    return stockList



def saveStock(stock):
    stockString = pickle.dumps(stock)
    return redisAccess.setValue(StockKey % stock.uid, stockString)

def removeStock(stock):
    return redisAccess.remove(StockKey % stock.uid)

def removeStockGroups(stockGroup):
    key = StockGroupKey % ('*',stockGroup.getGroupId())
    keys = redisAccess.getKeyMatching(key)
    stockGroup = redisAccess.getValue(keys[0])
    if stockGroup is not None:
        stockGroup = pickle.loads(stockGroup)
        return redisAccess.remove(StockGroupKey % (stockGroup.getGroupSize(),stockGroup.getGroupId()))
    return False

    return redisAccess.remove(key)

def getStockGroup( stockGroup):
    keys = redisAccess.getKeyMatching(StockGroupKey % ('*',stockGroup.getGroupId()))
    stockGroupList = []
    for key in keys:
        stockGroup = redisAccess.getValue(key)
        if stockGroup is not None:
            stockGroupList.append(pickle.loads(stockGroup))
    length = len(stockGroupList)
    if length > 0 and length < 2:
        return stockGroupList[0]
    elif length > 1:
        raise Exception("Something went wrong, got more than one objects with the same keys!")
    else:
        return None

def getAllStockGroupsByClass(weightClass):
    keys = redisAccess.getKeyMatching(StockGroupKey % (str(weightClass),'*'))
    stockGroupList = []

    for key in keys:
        stockGroup = redisAccess.getValue(key)
        if stockGroup is not None:
            stockGroupList.append(pickle.loads(stockGroup))
    return stockGroupList

def saveStockGroup(stockGroup):
    stockGroupString = pickle.dumps(stockGroup)
    return redisAccess.setValue(StockGroupKey % (stockGroup.getGroupSize(),stockGroup.getGroupId()), stockGroupString)

def saveCorelation(x, y, value):
    if x > y:
        temp = x
        x = y
        y = temp
    return redisAccess.setValue(CorrelationKey % (x,y), value)

def getCorelation(x, y):
    if x > y:
        temp = x
        x = y
        y = temp
    val = redisAccess.getValue(CorrelationKey % (x,y))
    if val is not None:
        return float(val)
    return None

def removeCorelation(x, y):
    if x > y:
        temp = x
        x = y
        y = temp
    return redisAccess.remove(CorrelationKey % (x,y))

