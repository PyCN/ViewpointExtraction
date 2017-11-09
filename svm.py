# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 09:49:57 2017

@author: Xie Yang
"""

from sklearn import svm
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import roc_curve
from sklearn.externals import joblib
import numpy as np
import time
import matplotlib.pyplot as plt
import extract

#保存训练好的svm模型
def saveModel(clf, file):
    joblib.dump(clf, file)
   
#导入本地svm模型
def loadModel(file):
    clf = joblib.load(file)
    return clf

#预测数据
def predict(clfFile, filePath, fileName):
    fn = fileName.split('.')[0]
    data = np.loadtxt(filePath+fn+"_向量.txt")
    clf = loadModel(clfFile)
    pre = clf.predict(data)
    extract.extract(pre, filePath, fileName)
    
#训练模型给用户
def train(fileName):
    #载入数据
    data = np.loadtxt(fileName)
    X = data[:, 1:]
    print("特征向量长度:", X.shape)
    y = data[:, 0]
    clf = svm.LinearSVC()
    #训练
    start = time.clock()
    clf.fit(X, y)
    end = time.clock()
    print("训练模型所用时间:", end-start)
    #保存模型
    saveModel(clf, "model/svmclf.pkl")
    
#n折交叉验证
def n_fold(filename, n=10):
    #载入数据
    data = np.loadtxt(filename)
    X = data[:, 1:]
    print("特征向量长度:", X.shape)
    y = data[:, 0]
    y_ans = []
    y_pre = []
    #n折交叉验证
    skf = StratifiedKFold(n)
    for train_index, test_index in skf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        #定义一个分类器，默认高斯分布
        clf = svm.LinearSVC()
        #训练模型，输入训练数据和对应标签
        clf.fit(X_train, y_train)
        y_ans.extend(y_test)
        #预测
        y_pre.extend(clf.predict(X_test))
        '''
        #画PR曲线
        y_score = clf.decision_function(X_test)
        precision, recall, _ = precision_recall_curve(y_test, y_score)
        plt.step(recall, precision, color='b', alpha=0.2, where='post')
        plt.fill_between(recall, precision, step='post', alpha=0.2, color='b')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title('2-class Precision-Recall curve: AP={0:0.2f}')
        #画ROC曲线
        y_score = clf.decision_function(X_test)
        fpr, tpr, thresholds = roc_curve(y_test, y_score, pos_label=1)
        plt.step(fpr, tpr, color='b', alpha=0.2, where='post')
        plt.fill_between(fpr, tpr, step='post', alpha=0.2, color='b')
        plt.xlabel('fpr')
        plt.ylabel('tpr')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title('2-class ROC curve: AP={0:0.2f}')
        '''
    #对十次交叉验证结果取平均值
    print(classification_report(y_ans, y_pre, digits=3))