# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 17:09:33 2017

@author: Xie Yang
"""

import jieba
import jieba.posseg as pseg
from sklearn.metrics import classification_report
import json
import os
import corpusProcess
import extract
    
#关键词+词性标注模式
def matchPOS(sentence):
    word_list = ["认为", "建议", "觉得", "坚称", "主张"]
    words = pseg.cut(sentence)
    for word, flag in words:
        if flag == 'v' and word in word_list:
            return True
    return False

#情感标注模式
def matchEmo(sentence):
    dictionary = []
    #载入情感词典
    with open('support/情感词典.txt', 'r', encoding="utf8") as f:
        for word in f:
            word = word.strip()
            dictionary.append(word)
    #分词
    word_list = jieba.cut(sentence)
    #统计句子中在情感词典中出现的个数
    count = 0
    for word in word_list:
        if word in dictionary:
            count += 1
    #5个时F1-score值最高
    if count >= 5:
        return True
    else:
        return False

#载入常见句法+依存关系模式
def loadCommon(parseFile, dependFile):
    #载入常见句法结构
    parseCommon = []
    with open("support/parseCommon.txt", 'r', encoding="utf8") as jf:
        for word in jf:
            word = word.strip()
            parseCommon.append(word)
    #载入常见依存关系
    dependCommon = []
    with open("support/dependCommon.txt", 'r', encoding="utf8") as jf:    
        for word in jf:
            word = word.strip()
            dependCommon.append(word)
    return parseCommon, dependCommon

#用户使用
def match(filePath, fileName):
    fn = fileName.split('.')[0]
    '''
    #生成parse和depend文件
    corpusProcess.segment(filePath+fileName, "data/"+fn+"_分词.txt")
    os.system("java -jar nlp.jar " + "data/ " + fn+"_分词.txt")
    os.remove("data/"+fn+"_分词.txt")
    corpusProcess.parse("data/"+fn+"_句法分析.txt", "data/"+fn+"_parse.txt")
    corpusProcess.depend("data/"+fn+"_依存关系.txt", "data/"+fn+"_depend.txt")
    '''
    #读取句子，parse和depend
    with open(filePath+fileName, 'r', encoding="utf8") as f:
        sentences = f.readlines()
    with open("data/"+fn+"_parse.txt", 'r', encoding="utf8") as pf:
        parseJson = pf.readlines()
    with open("data/"+fn+"_depend.txt", 'r', encoding="utf8") as df:
        dependJson = df.readlines()
    parseCommon, dependCommon = loadCommon("data/"+fn+"_parse.txt", "data/"+fn+"_depend.txt")
    #判断每句话是否符合模式
    vecPOS = []
    vecEmo = []
    vecPAD = []
    for i in range(len(sentences)):
        #是否符合关键词+词性标注模式
        if matchPOS(sentences[i]):
            vecPOS.append(1)
        else:
            vecPOS.append(0)
        #是否符合情感标注模式
        if matchEmo(sentences[i]):
            vecEmo.append(1)
        else:
            vecEmo.append(0)
        #是否符合句法+依存关系模式
        count = 0
        parse = json.loads(parseJson[i])
        for key in parse.keys():
            if key in parseCommon:
                count += 1
        depend = json.loads(dependJson[i])
        for key in depend.keys():
            if key in dependCommon:
                count += 1
        if count >= 35:
            vecPAD.append(1)
        else:
            vecPAD.append(0)
    #观点句抽取
    extract.extract(vecPOS, filePath, fileName)
    return vecPOS, vecEmo, vecPAD
    
#测试用
def evaluate(posFile, negFile):
    total_pos = 0
    total_neg = 0
    with open(posFile, 'r', encoding="utf8") as pf:
        for line in pf:
            total_pos += 1
    with open(negFile, 'r', encoding="utf8") as nf:
        for line in nf:
            total_neg += 1
    answer = [1 for i in range(total_pos)]
    answer = answer + [0 for i in range(total_neg)]
    posVecPOS, posVecEmo, posVecPAD = match("data/", "观点句.txt")
    negVecPOS, negVecEmo, negVecPAD = match("data/", "非观点句.txt")
    vecPOS = posVecPOS + negVecPOS
    vecEmo = posVecEmo + negVecEmo
    vecPAD = posVecPAD + negVecPAD
    vec = []
    for i in range(len(vecPOS)):
        if vecPOS[i] == 1 or vecPAD == 1:
            vec.append(1)
        else:
            vec.append(0)
    #print("关键词+词性标注：\n" + classification_report(answer, vecPOS, digits=10))
    #print("情感标注：\n" + classification_report(answer, vecEmo, digits=10))
    #print("句法+依存关系：\n" + classification_report(answer, vecPAD, digits=10))
    print("关键词+词性标注+情感标注：\n"+ classification_report(answer, vec, digits=10))

doc = "data/"
evaluate(doc+"观点句.txt", doc+"非观点句.txt")