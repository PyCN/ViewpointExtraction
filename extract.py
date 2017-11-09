# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 18:28:18 2017

@author: Xie Yang
"""

#从原文本中抽取出观点句
def extract(vec, filePath, fileName):
    with open(filePath+fileName, 'r', encoding="utf8") as fin:
        fn = fileName.split('.')[0]
        with open("output/"+fn+"_观点句抽取结果.txt", 'w', encoding="utf8") as fout:
            #输出值为1的句子
            i = 0
            for line in fin:
                if vec[i] == 1:
                    fout.write(line)
                i += 1