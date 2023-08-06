import DataTIC
from dataclasses import dataclass
from numpy import array as ndarray
from numpy import sqrt
import numpy


def getMeasuredProfileTICDataByRawTICData(rawBlockData):
    npRawData = ndarray(rawBlockData.matrix)
    
    measureBlock = __measureProfile__(npRawData, rawBlockData.descriptionTICData.timeSlice)
    
    return DataTIC.MeasureProfileTICData(rawBlockData.descriptionTICData, 
                                         measureBlock.countPerSlice, 
                                         measureBlock.meanPerSlice, 
                                         measureBlock.sigmaPerSlice, 
                                         measureBlock.errorSigmaPerSlice, 
                                         measureBlock.timePerSlice, 
                                         measureBlock.numberPerChannel, 
                                         measureBlock.countPerChannel, 
                                         measureBlock.matrix)

def __measureProfile__(rawArray, timeSlice):
    countChannel = rawArray[0].size
    countSlice = len(rawArray)
    
    countPerSlice = numpy.zeros(countSlice)
    meanPerSlice = numpy.zeros(countSlice, float)
    sigmaPerSlice = numpy.zeros(countSlice, float)
    errorSigmaPerSlice = numpy.zeros(countSlice, float)
    timePerSlice = numpy.zeros(countSlice, float)
    
    numberPerChannel = numpy.arange(countChannel)
    countPerChannel = numpy.zeros(countChannel)
    
    for i in range(0,countSlice):
        countPerSlice[i] = numpy.sum(rawArray[i])
        meanPerSlice[i] = numpy.median(rawArray[i])
        sigmaPerSlice[i] = numpy.std(rawArray[i])
        errorSigmaPerSlice[i] = sigmaPerSlice[-1]/sqrt(countPerSlice[-1])
        timePerSlice[i] = 0 + timeSlice*i

        countPerChannel = countPerChannel + rawArray[i]
    
    for i in range (0, countChannel):
        numberPerChannel[i] = i + 1
    return __BlockMeasuredProfile__(countPerSlice, meanPerSlice, sigmaPerSlice, errorSigmaPerSlice, timePerSlice)

def getMeasuredCounterTICDataByRawTICData(rawBlockData):
    measureBlock = __measureCounter__(rawBlockData)
    
    return DataTIC.MeasureCounterTICData(rawBlockData.descriptionTICData,
                                         measureBlock.sum)
    
def __measureCounter__(rawArray):
    return __BlockMeasuredCounter__(rawArray.sum())
    
@dataclass
class __BlockMeasuredCounter__():
    sum:int
    
@dataclass
class __BlockMeasuredProfile__():
    countPerSlice:ndarray
    meanPerSlice:ndarray
    sigmaPerSlice:ndarray
    errorSigmaPerSlice:ndarray
    timePerSlice:ndarray
        
if __name__ == '__main__':
    i=5