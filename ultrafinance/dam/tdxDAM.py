# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 23:42:53 2015

@author: pchaos
"""
import os

from ultrafinance.dam.baseDAM import BaseDAM
from ultrafinance.dam.tdxLib import TDXLib, TDXZXG
from ultrafinance.model import TICK_FIELDS, QUOTE_FIELDS, Quote, Tick
from ultrafinance.lib.errors import UfException, Errors
from os import path
import logging

LOG = logging.getLogger()


class TDXDAM(BaseDAM):
    ''' TDX DAO
    TDX 通达信
    '''
    QUOTE = 'quote'
    TICK = 'tick'

    def __init__(self):
        ''' constructor '''
        super(TDXDAM, self).__init__()
        #通达信数据根目录
        self.__TDXdir = None

    def targetPath(self, kind):
        return path.join(self.__TDXdir, "%s-%s.xls" % (self.symbol, kind))

    def __findRange(self, TDXLib, start, end):
        ''' return low and high as excel range '''
        inc = 1
        low = 0
        high = 0
        dates = TDXLib.readCol(0, 1)

        for index, date in enumerate(dates):
            if int(start) <= int(date):
                low = index + inc
                break

        if low:
            for index, date in reversed(list(enumerate(dates))):
                if int(date) <= int(end):
                    high = index + inc
                    break

        return low, high

    def __readData(self, basePath, start, end):
        '''
        从basePath目录查找通达信文件，read data
        '''
        ret = []
        if not path.exists(basePath):
            LOG.error("Target file doesn't exist: %s" % path.abspath(basePath))
            return ret
        with TDXLib(basePath, self.__symbol, TDXLib.READ_MODE) as TDX:
            ret = TDX.read(start, end)
        return ret

    def __writeData(self, targetPath, fields, rows):
        ''' write data '''
        if path.exists(targetPath):
            LOG.error("Target file exists: %s" % path.abspath(targetPath))
            raise UfException(Errors.FILE_EXIST, "can't write to a existing file")  # because xlwt doesn't support it

        with TDXLib(fileName=targetPath, mode=TDXLib.WRITE_MODE) as excel:
            excel.writeRow(0, fields)
            for index, row in enumerate(rows):
                excel.writeRow(index + 1, row)

    def readQuotes(self, start = None, end = None):
        ''' read symbols '''
        if type(start) == str:
            startInt = int(start)
            endInt = int(end)
        else:
            startInt = start
            endInt = end
        quotes = self.__readData(self.__TDXdir, startInt, endInt)
        return quotes

    def writeQuotes(self, quotes):
        ''' write symbols '''
        self.__writeData(self.targetPath(TDXDAM.QUOTE),
                         QUOTE_FIELDS,
                         [[getattr(quote, field) for field in QUOTE_FIELDS] for quote in quotes])

    def readTicks(self, start, end):
        ''' read ticks '''
        ticks = self.__readData(self.targetPath(TDXDAM.TICK), start, end)
        return [Tick(*tick) for tick in ticks]

    def writeTicks(self, ticks):
        ''' read symbols '''
        self.__writeData(self.targetPath(TDXDAM.TICK),
                         TICK_FIELDS,
                         [[getattr(tick, field) for field in TICK_FIELDS] for tick in ticks])

    def setDir(self, path, TDXDataBasePath = None):
        '''
        set dir
        path 通达信数据文件相对路径
        TDXDataBasePath 通达信数据文件根目录。例如：/home/yg/software/shared1/finacing/gtja/RichEZ/vipdoc
        '''
        if TDXDataBasePath is not None:
            path = os.path.join(TDXDataBasePath, path)
        if os.path.exists(path):
            self.__TDXdir = path
        else:
            raise UfException(Errors.INVALID_TDX_PATH, "通达信路径错误！\n{0}".format(path))

    def setSymbol(self, symbol):
        ''' set symbol '''
        self.__symbol = symbol

    def readZXG(self, fileName):
        '''
        读取通达信自选股
        :param fileName: 文件名
        :return:
        '''
        if os.path.exists(fileName):
            # 自选股文件存在
            tdxZXG = TDXZXG()
            zxg = tdxZXG.read(fileName)
            return zxg
        else:
            raise UfException(Errors.INVALID_TDX_PATH, "通达信自选股路径错误！\n{0}".format(path))
