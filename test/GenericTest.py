'''
Created on Feb 12, 2012

@author: arshadansari
'''
import unittest
from randomweightgenerator import WeightVectorGenerator
from portfoliomodule import StockCoRelation
from portfoliomodule import Stock
from portfoliomodule import StockGroup

class GenericTest(unittest.TestCase):

    def testStockCorelation(self):
        StockCoRelation.addCorelation('1', '2', 0)
        assert(StockCoRelation.getCorelation( '1', '2')==0)
        assert(StockCoRelation.getCorelation( '2', '1')==0)
        StockCoRelation.addCorelation('1', '3', 1)
        assert(StockCoRelation.getCorelation( '1', '3')==1)
        assert(StockCoRelation.getCorelation( '3', '1')==1)
        StockCoRelation.addCorelation('2', '1', 2)
        assert(StockCoRelation.getCorelation( '1', '2')==2)
        assert(StockCoRelation.getCorelation( '2', '1')==2)
        StockCoRelation.addCorelation('3', '2', 3)
        assert(StockCoRelation.getCorelation( '2', '3')==3)
        assert(StockCoRelation.getCorelation( '3', '2')==3)
        StockCoRelation.resetMatrix()
        #self.assertRaises(Exception, StockCoRelation.getCorelation( 'x', 'y'))

    def testWeightVectorGeneration(self):
        w = WeightVectorGenerator(100, 5, 0, 60)
        for i in range(0,100):
            (weightClass, weightVector) = w.getWeightVectorAndClassTuple()
            #print "%d %s" % (weightClass, weightVector)
            assert(weightClass > 0 and weightClass <= 5)
            assert(len(weightVector) == weightClass and sum(weightVector) == 100)

    def testStockGroupWeightGenerationWithRiskAndReward(self):
        listSize = 5
        stockList = []
        for i in range(0,listSize):
            stockList.append(Stock(str(i),'test'+str(i), (0.2+ 0.01*i), (0.1 + 0.01*i)))
        assert(len(stockList)==listSize)
        StockCoRelation.resetMatrix()
        for i in range(0,listSize):
            for j in range(i,listSize):
                StockCoRelation.addCorelation(stockList[i].uid, stockList[j].uid, 0)

        stockGroup = StockGroup(stockList)
        w = WeightVectorGenerator(100, listSize, 0, 65-listSize*3)
        weightCount = 0
        for i in range(0, 100):
            (weightClass, weightVector) = w.getWeightVectorAndClassTuple()
            while weightClass is not len(stockList):
                (weightClass, weightVector) = w.getWeightVectorAndClassTuple()
            weightCount += 1

            stockGroup.setPlotBestRewardByRisk( (weightClass, weightVector) )

        #print "%s" % (" \n".join([",".join([str(stock.uid), str(stock.reward), str(stock.risk)]) for stock in stockList]))
        #print "Weights created %s" % weightCount
        graphPlot = stockGroup.getPlotBestRewardByRisk()
        graphIndex = graphPlot.keys()
        graphIndex = sorted(graphIndex)
        for i in range(0, len(graphIndex)):
            print "%s %s" % (graphIndex[i], graphPlot[graphIndex[i]])
        assert('01234'== stockGroup.getGroupId())


    def testMetaStockGroupWeightGeneration(self):
        raise Exception("Not yet implemented!")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()