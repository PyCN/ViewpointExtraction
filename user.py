# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 17:23:15 2017

@author: Xie Yang
"""

import corpusProcess
import prepareVector
import pattern
import svm
import configparser

config = configparser.ConfigParser()
config.read('config.conf', encoding="utf8")
fileName = config['input']['fileName']
fn = fileName.split('.')[0]
filePath = config['input']['filePath']
mode = config['mode']['mode']

if mode == 'svm':
    corpusProcess.process(fileName, filePath)
    prepareVector.toVector(fileName, filePath)
    svm.predict("model/svmclf.clf", filePath, fileName)
elif mode == 'pattern':
    pattern.match(fileName, filePath)
elif mode == 'rf':
    pass
elif mode == 'ensemble':
    pass
else:
    print("请输入正确的模式！")