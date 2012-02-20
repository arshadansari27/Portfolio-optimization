'''
Created on Feb 12, 2012

@author: arshadansari
'''
import random, math

class StockGroup():
    '''
    Group of stock with collective risk and reward for given weightVector

    Gurantee is needed that the weight vector supplied has the class of group size

    '''
    def __init__(self, stockList, stockGroup = None):
        self.__stockList = stockList
        self.__groupId = StockGroup.generateId(stockList)
        if stockGroup is not None and stockGroup is not None and stockGroup.getGroupId is self.__groupId and stockGroup.getGroupSize == self.getGroupSize():
            self.__riskWiseRewardBestPlot = stockGroup.getPlotBestRewardByRisk()
            self.__vectorCount = stockGroup.getWeightVectorCount()
        else:
            self.__riskWiseRewardBestPlot = {}
            self.__vectorCount = 0
        self.__setPairsIn2()
        self.__thresholdLimitForWeightVector = len(stockList) * pow(10, (2 + len(stockList)))


    def getGroupSize(self):
        return len(self.__stockList)

    @staticmethod
    def generateId(stockList):
        keys = [elem.uid for elem in stockList]
        keys = sorted(keys)
        return "".join(keys)

    def isThresholdClear(self):
        if self.getWeightVectorCount() >= self.__thresholdLimitForWeightVector:
            return True
        return False

    def __setPairsIn2(self):
        pairs = []
        for i in range(0, len(self.__stockList)):
            for j in range(i+1, len(self.__stockList)):
                pairs.append( (self.__stockList[i],self.__stockList[j]))
        self.__stocksInPair = pairs

    def __getRewardForWeightVector(self, weightTuple):
        (weightClass, weightVector) = weightTuple
        summationReward = 0
        for i, stock in enumerate(self.__stockList):
            summationReward += (weightVector[i]/100.0) * stock.reward
        return round(summationReward,2)

    def __getStockByVectorValues(self, weightVector):
        stockSet = {}
        for idx, val in enumerate(weightVector):
            stockSet[self.__stockList[idx].uid] = (self.__stockList[idx], val)
        return stockSet

    def __getRiskForWeightVector(self, weightTuple):
        (weightClass, weightVector) = weightTuple
        if(len(self.__stockList) is not weightClass):
            raise Exception("Mismatch between weightClass and stock group size.")
        summationRisk = 0

        stockWiseWeightVector = self.__getStockByVectorValues(weightVector)
        for uid, (stock, weight) in stockWiseWeightVector.items():
            value = pow(weight/100.0,2) * pow(stock.risk,2)
            summationRisk += value

        for (stock1,stock2) in self.__stocksInPair:
            (x,stock1Val) = stockWiseWeightVector[stock1.uid]
            (y,stock2Val) = stockWiseWeightVector[stock2.uid]
            corelationVal = StockCoRelation.getCorelation(stock1.uid, stock2.uid)
            if corelationVal is None:
                corelationVal = 0
            value = 2 * (stock1Val/100.0) * stock1.risk * (stock2Val/100.0) * stock2.risk * corelationVal
            summationRisk += value
        return round(math.sqrt(summationRisk),2)

    def setPlotBestRewardByRisk(self, weightTuple):
        print "setting with weight Tuple %d:%s" % (weightTuple)
        reward = self.__getRewardForWeightVector(weightTuple)
        risk = self.__getRiskForWeightVector(weightTuple)
        if (self.__riskWiseRewardBestPlot.has_key(risk) and self.__riskWiseRewardBestPlot[risk]['REWARD']>reward):
            return
        (weightClass, weightVector) = weightTuple
        self.__riskWiseRewardBestPlot[risk] = {'GROUPID': self.getGroupId(), 'REWARD': reward, 'WeightVector': weightVector}
        if(self.__vectorCount is None):
            self.__vectorCount = 0
        self.__vectorCount += 1

    def getWeightVectorCount(self):
        if(self.__vectorCount is None):
            self.__vectorCount = 0
        return self.__vectorCount

    def getPlotBestRewardByRisk(self):
        return self.__riskWiseRewardBestPlot

    def getGroupId(self):
        if self.__groupId is not None:
            self.__groupId = StockGroup.generateId(self.__stockList)
        return self.__groupId

    def __str__(self) :
        return str(self.__groupId)

    def __eq__(self, other) :
        return self.__groupId == other.__groupId


class MetaStockGroup():
    '''
    Using composition to handle all the possible sub groups of the given stocklist
    '''

    def __init__(self):
        self.__stockGroups = {}
        self.__graphDataForStockGroups = {}

    def addStockGroups(self, stockGroup):
        if self.__stockGroups[stockGroup.getGroupSize()] is None:
            self.__stockGroups[stockGroup.getGroupSize()] = {}
        self.__stockGroups[stockGroup.getGroupSize()][stockGroup.getGroupId()] = stockGroup

    def getPlotBestRewardByRisk(self):
        for weightClass in self.__stockGroups.keys():
            for key in self.__stockGroups[weightClass].keys():
                graph = self.__stockGroups[weightClass][key].getPlotBestRewardByRisk()
                for risk, data in graph.items():
                    if self.__graphDataForStockGroups.has_key(risk) and self.__graphDataForStockGroups[risk]['REWARD'] > data['REWARD']:
                        continue
                    else:
                        self.__graphDataForStockGroups[risk] = data
        return self.__graphDataForStockGroups



class Stock():
    '''
    Entity object
    '''

    def __init__(self, uid, name, reward, risk):
        self.uid = uid
        self.name = name
        self.reward = reward
        self.risk = risk

    def __str__(self) :
        return str(self.uid) # +": " + self.name

    def __eq__(self, other) :
        return self.uid == other.uid



class StockCoRelation:

    __correlationMatrix = {}

    @staticmethod
    def resetMatrix():
        StockCoRelation.__correlationMatrix = {}

    @staticmethod
    def getCorelationMatrix():
        return StockCoRelation.__correlationMatrix

    @staticmethod
    def setCorelationMatrix(correlationMatrix):
        StockCoRelation.__correlationMatrix = correlationMatrix

    @staticmethod
    def addCorelation( firstStock, secondStock, correlationValue):
        if firstStock==secondStock: correlationValue = 1
        if not StockCoRelation.__correlationMatrix.has_key(firstStock):
            StockCoRelation.__correlationMatrix[firstStock] = {}
        if not StockCoRelation.__correlationMatrix.has_key(secondStock):
            StockCoRelation.__correlationMatrix[secondStock] = {}
        StockCoRelation.__correlationMatrix[firstStock][secondStock] = correlationValue
        StockCoRelation.__correlationMatrix[secondStock][firstStock] = correlationValue

    @staticmethod
    def getCorelation(firstStock, secondStock):
        if StockCoRelation.__correlationMatrix.has_key(firstStock) and StockCoRelation.__correlationMatrix[firstStock].has_key(secondStock):
            return StockCoRelation.__correlationMatrix[firstStock][secondStock]
        else:
            return None
            #raise Exception("Co relation does not exist yet!")
