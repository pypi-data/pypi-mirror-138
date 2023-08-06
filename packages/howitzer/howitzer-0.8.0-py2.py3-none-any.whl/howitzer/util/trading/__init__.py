from datetime import datetime, timedelta, timezone, tzinfo
from howitzer.util.date import shortStringFormat
from howitzer.util.trading.indicators import *
from os.path import join
import dateutil.parser as dateparse
import numpy as np
import ujson as json
import math

time_index = 0
low_index = 1
high_index = 2
open_index = 3
close_index = 4
volume_index = 5

class Candle:
    def __init__(self, currentData: list, previousClose: float = None):
        self.time = datetime.fromtimestamp(currentData[time_index], tz=timezone.utc)
        self.low = currentData[low_index]
        self.high = currentData[high_index]
        self.open = currentData[open_index]
        self.close = currentData[close_index]
        self.volume = currentData[volume_index]
        self.percent = 100 * (self.close - self.open) / self.open
        self.diff = self.close - self.open
        self.range = self.high - self.low
        self.green = self.close > self.open
        self.red = self.close < self.open
        self.head = self.high - max(self.close, self.open)
        self.tail = min(self.open, self.close) - self.low
        self.body = max(self.close, self.open) - min(self.close, self.open)
        self.twap = (self.close + self.high + self.low) / 3
        self.tr = self.range
        if previousClose is not None:
            self.tr = max(self.range, abs(self.high-previousClose),
                          abs(self.low-previousClose))

    def getTimeStr(self):
        return self.time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

class Chart:
    def __init__(self, _rawCandleData: list):
        number_of_candles_to_parse = len(_rawCandleData)
        self.candles = []
        self.fast_candles = np.array(_rawCandleData)
        for i in range(number_of_candles_to_parse):
            if i < number_of_candles_to_parse - 1:
                self.candles.append(
                    Candle(_rawCandleData[i], previousClose=_rawCandleData[i+1][close_index]))
            else:
                self.candles.append(Candle(_rawCandleData[i]))

    def Aroon(self, length: int = None, offset: int = 0):
        # offset added to match trading view
        targetTimeFrame = self.PreProcess(length+1, offset)
        return Aroon(candles=targetTimeFrame)

    def EMA(self, length: int = None, lookback: int = math.inf, offset: int = 0, lhoc: str = "close"):
        targetTimeFrame = self.candles[offset:]
        return ema(targetTimeFrame, length, lookback, lhoc)

    def IndexOfHighest(self, length: int = None, offset: int = 0, lhoc: str = "high"):
        return np.argmax(self.PreProcessFast(length, offset, lhoc))
    
    def Highest(self, length: int = None, offset: int = 0, lhoc: str = "high"):
        return np.max(self.PreProcessFast(length, offset, lhoc))

    def IndexOfLowest(self, length: int = None, offset: int = 0, lhoc: str = "low"):
        return np.argmin(self.PreProcessFast(length, offset, lhoc))

    def Lowest(self, length: int = None, offset: int = 0, lhoc: str = "low"):
        return np.min(self.PreProcessFast(length, offset, lhoc))

    def SMA(self, length: int = None, offset: int = 0, lhoc: str = "close"):
        return np.average(self.PreProcessFast(length, offset, lhoc))
       
    def PreProcessFast(self, length:int, offset:int=0, lhoc: str = "close"):
        length = len(self.candles) if length is None else length

        offset = 0 if offset is None else abs(offset)

        index = close_index
        if lhoc == "low":
            index = low_index
        elif lhoc == "high":
            index = high_index
        elif lhoc == "open":
            index = open_index
        elif lhoc == "volume":
            index = volume_index

        return self.fast_candles[offset:offset+length,index]

    def PreProcess(self, length, ofs):
        if length is None:
            length = len(self.candles)
        if length > len(self.candles):
            raise "Not enough candles"
        offset = 0 if ofs is None else abs(ofs)
        targetTimeFrame = self.candles[offset: offset + length]
        return targetTimeFrame


def chartFromDataFiles(pathToDataFolder: str, startDate: datetime, endDate: datetime):
    def BLANK_CANDLE():
        return [0, math.inf, 0, 0, 0, 0]

    stopTime = endDate.timestamp()
    dailyRawCandles = []
    # todo: add days to queu and then deque on multiple threads to get data, sort after the fact
    while(startDate.timestamp() <= stopTime):
        tempDaily = BLANK_CANDLE()
        nextDay = startDate + timedelta(days=1)

        targetFileName = shortStringFormat(startDate) + ".json"
        targetFilePath = join(pathToDataFolder, targetFileName)
        f = open(targetFilePath)

        data = json.load(f)
        # daily logic
        tempDaily[time_index] = dateparse.parse(data[0]["time"]).timestamp()
        tempDaily[open_index] = data[0]["open"]
        for minute in data:
            candleTime = dateparse.parse(minute["time"])
            if candleTime.timestamp() < nextDay.timestamp():
                tempDaily[volume_index] += minute["volume"]
                tempDaily[close_index] = minute["close"]
                tempDaily[high_index] = max(tempDaily[high_index], minute["high"])
                tempDaily[low_index] = min(tempDaily[low_index], minute["low"])

        dailyRawCandles.append(tempDaily)
        startDate = nextDay
        f.close()

    dailyRawCandles.reverse()

    return {
        "daily": Chart(dailyRawCandles)
    }
