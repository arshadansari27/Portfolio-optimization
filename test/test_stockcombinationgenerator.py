'''
Created on Feb 15, 2012

@author: arshadansari
'''
import unittest
from stockcombinationgenerator import getCombination, addStock
from portfoliomodule import Stock
from integration import getAllStocks, removeStock, saveStock,\
    getAllStockGroupsByClass, removeStockGroups

class Test(unittest.TestCase):

    @unittest.skip("skipping")
    def testCombinationGeneration(self):
        listSize = 5
        stockList = []
        print "Current Stocks: "
        for i in range(0,listSize):
            stockList.append(Stock(str(i),'test'+str(i), (0.2+ 0.01*i), (0.1 + 0.01*i)))
        print "%s" % " ".join([str(elem) for elem in stockList])
        newStock = Stock('x','newSTock', 0.0, 0.0)
        print "Adding new Stock:%s" % newStock
        combinations = getCombination(newStock, stockList)
        groupIds = combinations.keys()[:]
        print "Total combinations : %d " % len(groupIds)


    def testAddStock(self):

        print "Current Stocks: "
        print "%s" % ("\n".join([str(elem) for elem in getAllStocks()]))
        stockList = []
        print "Adding stocks..."
        for i in range(0,10):
            stock = Stock(str(i),'test'+str(i), (0.2+ 0.01*i), (0.1 + 0.01*i))
            stockList.append(stock)
            addStock(stock)
            #addStock()
        storedStocks = getAllStocks()
        for stock in storedStocks:
            print "Stored : %s" % stock

        for i in range(0,12):
            storedStockGroups = getAllStockGroupsByClass(i)
            for stockGroup in storedStockGroups:
                print stockGroup.getGroupId()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCombinationGeneration']
    unittest.main()