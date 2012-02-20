'''
Created on Feb 14, 2012

@author: arshadansari
'''
from randomweightgenerator import startSubscriber
from randomweightgenerator import expectedSize
from integration import getAllStockGroupsByClass, saveStockGroup
from portfoliomodule import StockGroup


def stockGroupWeightUpdater(weightClass, weightVector):
    stockGroups = getAllStockGroupsByClass(weightClass)
    for stockGroup in stockGroups:
        stockGroup.setPlotBestRewardByRisk((weightClass, weightVector,))
        if (stockGroup.isThresholdClear()):
            notifyExpectants(stockGroup)
        saveStockGroup(stockGroup)
    print stockGroups

def notifyExpectants(stockGroup):
    pass

if __name__ == '__main__':
    print expectedSize
    def callBack((wC,wV,)):
        print "Received %d => %s" % (wC, wV)
        stockGroupWeightUpdater(wC, wV)

    for i in range(2, expectedSize):
        print "Starting subscriber :%d" % i
        startSubscriber(i, callBack)

    while 1:
        pass