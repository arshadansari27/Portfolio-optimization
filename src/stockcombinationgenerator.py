'''
Created on Feb 14, 2012

@author: arshadansari
'''
from integration import saveStockGroup,getAllStocks,saveStock, saveCorelation
from portfoliomodule import StockGroup, StockCoRelation


def addStock(newStock):
    listOfStocks = getAllStocks()
    saveStock(newStock)
    print "Added stock %s" % newStock
    if len(listOfStocks) is not 0:
        combinationsOfStockGroup = getCombination(newStock, listOfStocks)
        print combinationsOfStockGroup
        for stockGroup in combinationsOfStockGroup.values():
            saveStockGroup(stockGroup)

def addStockCorelation(stock1, stock2, correlationValue):
    StockCoRelation.addCorelation(stock1.uid, stock2.uid, correlationValue)
    saveCorelation(stock1.uid, stock2.uid, correlationValue)

def getCorelation(stock1, stock2):
    val = StockCoRelation.getCorelation(stock1.uid, stock2.uid)
    if val is None:
        val = getCorelation(stock1.uid, stock2.uid)
    return val

def getCombination(newStock, listOfStocks):
    combinationStockGroupList = {}
    queue = []
    currentStockList = []
    queue.append((0,[newStock]))
    count = 0
    while len(queue) is not 0:
        (startPoint, currentStockList) = queue.pop()
        stockGroup = StockGroup(currentStockList)
        print "Got combination of size: %d" % len(currentStockList)
        combinationStockGroupList[stockGroup.getGroupId()] = stockGroup
        newStockGroupList = []

        for i in range(startPoint, len(listOfStocks)):
            newStockGroupList = currentStockList[:]
            newStockGroupList.append(listOfStocks[i])
            queue.append((i+1,newStockGroupList,))
        count += 1
    print "********* Count of total combinations %d for length %d" % (count, len(combinationStockGroupList))
    return combinationStockGroupList



if __name__ == '__main__':
    pass