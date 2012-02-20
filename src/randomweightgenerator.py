'''
Created on Feb 14, 2012

@author: arshadansari
'''
import redis, pickle, random
import thread, time

runningPublisher = True
maxValue = 100
expectedSize = 10
mean = 0
deviation = abs(60 - 3 * expectedSize) + 1
delay = 1

def startGeneration():
    try:
        thread.start_new_thread( generator )
    except:
        print "Error: unable to start thread for the publisher"

def startSubscriber(weightClass, callBack):
    try:
        thread.start_new_thread( subscriber ,(weightClass, callBack,))
    except:
        print "Error: unable to start thread for subscriber on channel {%d}" % weightClass

def generator():
    weightGenerator = WeightVectorGenerator(maxValue, expectedSize, mean, deviation)
    rObj = redis.Redis()
    while runningPublisher:
        time.sleep(delay)
        (weightClass, weightVector) = weightGenerator.getWeightVectorAndClassTuple()
        print "Publishing %d => %s" % (weightClass, weightVector)
        rObj.publish('WEIGHTVECTOR'+str(weightClass), pickle.dumps(weightVector))

def subscriber(classToSubscribe, callBack):
    rObj = redis.Redis()
    subscriber = rObj.pubsub()
    subscriber.subscribe('WEIGHTVECTOR'+str(classToSubscribe))
    for message in subscriber.listen():
        #print "Receiving %s" % pickle.loads(message['data'])
        callBack((classToSubscribe, pickle.loads(message['data'])))


class WeightVectorGenerator(object):
    '''
    classdocs
    TODO: Change the mean and deviation to handle changing expectedSize.
    The greater the expected size, the lesser the standard deviation
    '''


    def __init__(self, maxValue, expectedSize, mean=0, deviation=60):
        '''
        Constructor
        '''
        self.maximumValue = maxValue
        self.expectedSize = expectedSize
        self.mean = mean
        self.deviation = deviation

    def __getNextRandomNumber(self):
        val = random.normalvariate(self.mean, self.deviation)
        while abs(val) > self.maximumValue:
            val = random.normalvariate(self.mean, self.deviation)
        return int(abs(val))

    def __getWeightVector(self):
        remaining = self.maximumValue
        weightVector = []

        for i in range(0, self.expectedSize):
            nextRandom = self.__getNextRandomNumber()
            if remaining < 0:
                weightVector.append(0)
                continue
            if (remaining - nextRandom) < 0 or i == (self.expectedSize-1):
                weightVector.append(remaining)
            else:
                weightVector.append(nextRandom)
            remaining -= nextRandom

        random.shuffle(weightVector)
        return weightVector

    def __getClassSize(self, weightVector):
        weightClass = 0
        for item in weightVector:
            if item == 0:
                continue
            else:
                weightClass += 1
        return weightClass

    def getWeightVectorAndClassTuple(self):
        weightVector = self.__getWeightVector()
        weightClass = self.__getClassSize(weightVector)
        weightVector = [weight for weight in weightVector if weight is not 0]
        return (weightClass, weightVector)

if __name__ == "__main__":
    generator()