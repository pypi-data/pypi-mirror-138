'''
Created on Dec 28, 2021

@author: Dmitry
'''

from dataclasses import dataclass
from datetime import datetime as dt
from enum import Enum
from numpy import ndarray


#import array
@dataclass
class DescriptionTICData:

    def __init__(self, dateTime, timeSlice, delay, countChannel, countSlice, threshold):
        self.dateTime = dateTime
        self.timeSlice = timeSlice
        self.delay = delay
        self.countChannel = countChannel
        self.countSlice = countSlice
        self.threshold = threshold

    dateTime: dt
    timeSlice: float
    delay: float
    countChannel: int
    countSlice: int
    threshold: ndarray

@dataclass
class DescriptionDevice:
    name: str
    channelFrom: int
    channelTo: int
    

@dataclass
class RawTICData:
    descriptionTICData: DescriptionTICData
    matrix: ndarray
    
@dataclass
class MeasureProfileTICData:

    def __init__(self, descriptionTICData, countPerSlice, meanPerSlice, sigmaPerSlice, errorSigmaPerSlice, timePerSlice, numberPerChannel, countPerChannel, matrix):
        self.descriptionTICData = descriptionTICData
        self.countPerSlice = countPerSlice
        self.meanPerSlice = meanPerSlice
        self.sigmaPerSlice = sigmaPerSlice
        self.errorSigmaPerSlice = errorSigmaPerSlice
        self.timePerSlice = timePerSlice
        self.numberPerChannel = numberPerChannel
        self.countPerChannel = countPerChannel
        self.matrix = matrix

    descriptionTICData: DescriptionTICData
    countPerSlice: ndarray
    meanPerSlice: ndarray
    sigmaPerSlice: ndarray
    errorSigmaPerSlice: ndarray
    timePerSlice: ndarray
    numberPerChannel: ndarray
    countPerChannel: ndarray
    matrix: ndarray
    
class MeasureProfileTypeEnum(Enum):
    COUNTPERSLICE = (0, "Count per slice", 'Time', "Sec", "Count", "")
    MEANPERSLICE =  (1, "Count average per slice", "Time", "Sec", "Count average", "")
    SIGMAPERSLICE = (2, "Sigma count averge per slice", "Time", "Sec", "Sigma count", "")
    COUNTPERCHANNEL = (3, "Count per channel", "Channel", "", "Count", "")
    MATRIX = (4, "Profile", "Time", "Sec", "Channel", "", "Count", "")
    
    def __init__(self, id, title, nameX, unitX, nameY, unitY, nameColor = "", unitColor = ""):
        self.id = id
        self.title = title
        self.nameX = nameX
        self.unitX = unitX
        self.nameY = nameY
        self.unitY = unitY
        self.nameColor = nameColor
        self.unitColor = unitColor

class MeasureWaveDetectorsEnum(Enum):
    FIRSTSDETECTOR = (0, "Right-Up", 'Time', "Sec", "Count", "")
    SECONDSDETECTOR =  (1, "Right-Bottom", 'Time', "Sec", "Count", "")
    THIRDSDETECTOR = (2, "Left-Bottom", 'Time', "Sec", "Count", "")
    FOURTHSDETECTOR = (3, "Left-Up", 'Time', "Sec", "Count", "")
    FIFTHSDETECTOR = (4, "Center", 'Time', "Sec", "Count", "")
    ALLDETECTOR = (4, "All", 'Time', "Sec", "Count", "")
    
    def __init__(self, id, title, nameX, unitX, nameY, unitY, nameColor = "", unitColor = ""):
        self.id = id
        self.title = title
        self.nameX = nameX
        self.unitX = unitX
        self.nameY = nameY
        self.unitY = unitY
        self.nameColor = nameColor
        self.unitColor = unitColor
    
@dataclass
class MeasureCounterTICData:
    descriptionTICData: DescriptionTICData
    sum: int
    countPerSlice: ndarray
    
    
@dataclass
class DownloadData:
    id:int
    acsn:int
    dateTime:str
    delay:float
    timeslice:float
    threshold: ndarray
    matrix:ndarray