'''
Created on Feb 14, 2012

@author: arshadansari
'''
import unittest

from portfoliomodule import StockCoRelation
from portfoliomodule import Stock
from portfoliomodule import StockGroup
from portfoliomodule import MetaStockGroup
from integration import saveStock, getStock, removeStock,\
    saveStockGroup, getStockGroup, removeStockGroups, getAllStocks, saveCorelation, getCorelation,\
    removeCorelation, getAllStockGroupsByClass, StockKey, StockGroupKey,\
    CorrelationKey
from unittest.case import SkipTest

class DBAccessTest(unittest.TestCase):

    def setUp(self):
        pass

    def testStockAddingAndRemoving(self):
        stock = Stock(str(9),'test9', (0.2+ 0.01), (0.1 + 0.01))
        assert(saveStock(stock) is True)
        stock2 = getStock(stock)
        assert(stock2 is not None and stock2 == stock)
        val = removeStock(stock2)
        assert(val is True)
        stock2 = getStock(stock)
        assert(stock2 is None)
        assert(saveStock(stock) is True)
        stock2 = Stock(str(8),'test8', (0.2+ 0.01), (0.1 + 0.01))
        assert(saveStock(stock2) is True)
        stockList = getAllStocks()
        assert(len(stockList) >=2 )
        val = False
        for stockReturned in stockList:
            val = val or stockReturned.uid in ['9','8']
        assert(val is True)
        for stockReturned in stockList:
            assert(removeStock(stockReturned) is True)


    def testStockGroupAddingAndRemoving(self):
        stock1 = Stock(str(1),'test1', (0.2+ 0.01), (0.1 + 0.01))
        stock2 = Stock(str(2),'test2', (0.2+ 0.01), (0.1 + 0.01))
        stock3 = Stock(str(3),'test3', (0.2+ 0.01), (0.1 + 0.01))
        assert ( saveStock(stock1) is True)
        assert ( saveStock(stock2) is True)
        assert ( saveStock(stock3) is True)
        stockGroupList = [stock1, stock2, stock3]
        stockGroup = StockGroup(stockGroupList)
        assert( saveStockGroup(stockGroup) is True)
        lookupStockGroup = getStockGroup(stockGroup)
        assert(lookupStockGroup is not None)
        assert(removeStockGroups(lookupStockGroup) is True)
        lookupStockGroup = getStockGroup(stockGroup)
        assert(lookupStockGroup is None)
        assert(removeStock(stock1) is True)
        assert(removeStock(stock2) is True)
        assert(removeStock(stock3) is True)

    def testStockCorelation(self):
        stock1 = Stock('T1','test1', (0.2+ 0.01), (0.1 + 0.01))
        stock2 = Stock('T2','test2', (0.2+ 0.01), (0.1 + 0.01))

        assert( saveCorelation(stock1.uid, stock2.uid, -1) is True)
        assert( getCorelation(stock1.uid, stock2.uid) == -1)
        assert( removeCorelation(stock1.uid, stock2.uid))
        assert( getCorelation(stock1.uid, stock2.uid) is None)

    @unittest.skip("skipping")
    def testToRemoveAllStocksAndGroups(self):
        stocks = getAllStocks()
        for stock in stocks:
            removeStock(stock)
        for i in range(0,12):
            stockGroups = getAllStockGroupsByClass(i)
            for stockGroup in stockGroups:
                removeStockGroups(stockGroup)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()