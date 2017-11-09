#-*- coding:utf-8 -*-

import numpy as np
import time
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble.forest import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.externals import joblib
#n折交叉验证
def RF_n_fold(filename,n=10):
    '''
    默认10折交叉验证
    :param filename: 特征矩阵文件（包含四种特征{句法特征 依存关系特征 TF-IDF特征 词现特征} 相互组合）
    :param n:将特征矩阵分成的份数
    :return:
    '''
    #加载数据
    data = np.loadtxt(filename)
    X = data[:, 1:]
    y = data[:, 0]
    print(y)
    print("特征矩阵形状：")
    print(X.shape)
    #正确标签
    y_ans = []
    #预测标签
    y_pre = []
    print("开始进行%d折交叉验证....[RF模型]"%n)
    start = time.clock()
    skf = StratifiedKFold(n_splits=n,shuffle=True)
    for train_index,test_index in skf.split(X,y):
        X_train,X_test = X[train_index],X[test_index]
        y_train,y_test = y[train_index],y[test_index]
        #实例化RandomForestClassification对象
        #全部使用默认值
        clf = RandomForestClassifier()
        clf.fit(X_train,y_train)
        y_ans.extend(y_test)
        y_pre.extend(clf.predict(X_test))
        #PR曲线图
        pass
        #ROC曲线图
        pass

    end = time.clock()
    print("%d-折交叉验证完成 ! [RF模型]"%n)
    print("%d-折交叉验证的运行时间: %f"%(n,end-start))
    print("分类报告保存至log文件夹下的RF_%d_折交叉验证分类报告.txt"%n)
    target_name = ['非观点句','观点句']
    print(classification_report(y_ans,y_pre,digits=10,target_names=target_name))
    # with open("log/RF_10_折交叉验证分类报告.txt",'w') as f:
    #     pass

#保存训练模型
def savemodel(clf,filename):
    joblib.dump(clf,filename+".pkl")

#加载训练模型
def loadmodel(filename):
    clf = joblib.load(filename+".pkl")
    return clf

#预测数据(需要修改)
def predict(clf,datafile):
    data = np.loadtxt(datafile)
    pre = clf.predict(data)
    return pre