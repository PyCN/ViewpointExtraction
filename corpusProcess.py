# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 14:56:32 2017

@author: Xie Yang
"""

import tool
import json
import re
import jieba
import os

#加载自定义停用词表
def loadStopWordsList(stopwordFile):
    with open(stopwordFile, 'r') as f:
        stopwords = [line.strip() for line in f]
        return stopwords

#分词
def segment(inputFile, outputFile):
    with open(inputFile, 'r', encoding="utf8") as fin:
        with open(outputFile, 'w', encoding="utf8") as fout:
            #对文本中的每一行（即每句话）进行分词，并输出到输出文件
            for line in fin:
                line = line.strip()
                word_list = jieba.cut(line)
                fout.write(" ".join(word_list).strip())
                fout.write('\n')

#分词且去掉停用词
def segmentWithoutStopWords(inputFile, outputFile, stopwordFile):
    with open(inputFile, 'r', encoding="utf8") as fin:
        with open(outputFile, 'w', encoding="utf8") as fout:
            #这里加载停用词的路径
            stopwords = loadStopWordsList(stopwordFile)
            #对文本中的每一行（即每句话）进行分词，并输出到输出文件
            for line in fin:
                line = line.strip()
                word_list = jieba.cut(line)
                outstr = ""
                for word in word_list:
                    if word not in stopwords:
                        outstr += word + ' '
                fout.write(outstr.strip() + '\n')

#用户使用时用               
def process(fileName, filePath):
    fn = fileName.split('.')[0]
    #分词
    segmentWithoutStopWords(filePath+fileName, filePath+fn+"_分词.txt", "support/哈工大停用词表.txt")
    print("分词处理完毕！")
    