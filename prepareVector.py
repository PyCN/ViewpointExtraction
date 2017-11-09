# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 10:46:58 2017

@author: Xie Yang
"""

import json
import re
import os
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

#从json格式文件载入字典
def loadDict(jsonFile):
    with open(jsonFile, 'r', encoding="utf8") as jf:
        dictionary = json.load(jf)
        return dictionary

#保存字典到json格式文件
def saveDict(dictionary, jsonFile):
    with open(jsonFile, 'w', encoding="utf8") as jf:
        json.dump(dictionary, jf)

#得到词袋模型的词典
def getWordBagDict(file):
    #构建词典
    wordBagDict = {}
    with open(file, 'r', encoding="utf8") as f:
        for line in f:
            line = line.strip().split(' ')
            first = True
            for word in line:
                #跳过分类标签
                if first:
                    first = False
                    continue
                if word not in wordBagDict:
                    wordBagDict[word] = 1
                else:
                    wordBagDict[word] += 1
    return wordBagDict

#句子转化成词袋向量
def toWordBagVec(wordBagDict, inputFile, outputFile):
    with open(inputFile, 'r', encoding="utf8") as fin:
        with open(outputFile, 'w', encoding="utf8") as fout:
            wordBagDict = list(wordBagDict)
            for line in fin:
                line = line.split(' ')
                #跳过第一个分类标签
                label = line[0]
                line = line[1:]
                #初始化向量
                wordBagVec = [0 for i in range(len(wordBagDict))]
                #构建特征向量
                for word in line:
                    if word in wordBagDict:
                        wordBagVec[wordBagDict.index(word)] = 1
                #训练时有标签，使用时没有标签
                outstr = str(label)
                for e in wordBagVec:
                    outstr += ' ' + str(e)
                fout.write(outstr+'\n')
                
#句子转化成tf-idf向量
def toTFIDFVec(inputFile, outputFile):
    with open(inputFile, 'r', encoding="utf8") as fin:
        corpus = []
        labelVec = []
        for line in fin:
            labelVec.append(line[0])
            line = line[2:]
            corpus.append(line)
        #当前文件路径
        #path = os.path.dirname(os.path.abspath(__file__))
        #判断特征向量的对象是否已经序列化下来，若存在 加载进来直接对文本提取TF-IDF特征矩阵
        if os.path.exists("support/tfidf_vectorizer.pkl"):
            with open('support/tfidf_vectorizer.pkl', 'rb') as f:
                tfidf_vectorizer = pickle.load(f)
                tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
                words = tfidf_vectorizer.get_feature_names()
                weight = tfidf_matrix.toarray()
            with open(outputFile, 'w', encoding="utf8") as fout:
                #遍历所有文本
                for i in range(len(weight)):
                    fout.write(labelVec[i])
                    #遍历某一类文本下的词语权重
                    for j in range(len(words)):
                        fout.write(' ' + str(weight[i][j]))
                    fout.write('\n')
        #若不存在 则创建TfidfVectorizer 并对训练集数据特区特征矩阵后将对象序列化下来 方便下次直接使用
        else:
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_vectorizer.fit(corpus)
            #保存
            with open("support/tfidf_vectorizer.pkl",'wb') as f:
                pickle.dump(tfidf_vectorizer, f)
            tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
            words = tfidf_vectorizer.get_feature_names()
            weight = tfidf_matrix.toarray()
            print(weight.shape)
            with open(outputFile, 'w', encoding="utf8") as fout:
                #遍历所有文本
                for i in range(len(weight)):
                    fout.write(labelVec[i])
                    #遍历某一类文本下的词语权重
                    for j in range(len(words)):
                        fout.write(' ' + str(weight[i][j]))
                    fout.write('\n')
        
#组合特征向量
def combine4Vec(file1, file2, file3, file4, file5):
    vec1 = np.loadtxt(file1)
    vec2 = np.loadtxt(file2)
    vec3 = np.loadtxt(file3)
    vec4 = np.loadtxt(file4)
    #如果是多维向量
    if vec1.ndim > 1:
        label = vec1[:, 0]
        vec1 = vec1[:, 1:]
        vec2 = vec2[:, 1:]
        vec3 = vec3[:, 1:]
        vec4 = vec4[:, 1:]
        print(label.shape, vec1.shape, vec2.shape, vec3.shape, vec4.shape)
        vec = np.hstack((np.transpose([label]), vec1, vec2, vec3, vec4))
    #如果是一维向量
    else:
        label = vec1[0]
        vec1 = vec1[1:]
        vec2 = vec2[1:]
        vec3 = vec3[1:]
        vec4 = vec4[1:]
        vec = np.append(vec1, vec2)
        vec = np.append(vec, vec3)
        vec = np.append(vec, vec4)
        vec = np.append(label, vec)
    np.savetxt(file5, vec);
    
#组合特征向量
def combine2Vec(file1, file2, file5):
    vec1 = np.loadtxt(file1)
    vec2 = np.loadtxt(file2)
    #如果是多维向量
    if vec1.ndim > 1:
        label = vec1[:, 0]
        vec1 = vec1[:, 1:]
        vec2 = vec2[:, 1:]
        print(label.shape, vec1.shape, vec2.shape)
        vec = np.hstack((np.transpose([label]), vec1, vec2))
    #如果是一维向量
    else:
        label = vec1[0]
        vec1 = vec1[1:]
        vec2 = vec2[1:]
        vec = np.append(vec1, vec2)
        vec = np.append(label, vec)
    np.savetxt(file5, vec);

#给用户用
def toVector(fileName, filePath):
    fn = fileName.split('.')[0]
    #载入词典
    wordBagDict = loadDict("support/分词词典.txt")
    print("词典载入完成！")
    #构建观点句向量
    toWordBagVec(wordBagDict, filePath+fn+"_分词.txt", filePath+fn+"_wordBag_向量.txt")
    toTFIDFVec(filePath+fn+"_分词.txt", filePath+fn+"_tfidf_向量.txt")
    combine2Vec(filePath+fn+"_wordBag_向量.txt", filePath+fn+"_tfidf_向量.txt", filePath + fn+"_向量.txt")
    print("向量构建完成！")
