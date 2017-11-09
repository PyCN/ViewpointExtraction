# -*- coding: utf-8 -*-
"""
Created on Sat May  9 17:16:24 2015

@author: archer
"""
import re
from collections import deque
import os
import json

def fenduan(data):
    return data.replace('(ROOT [18.586]\n  (FRAG [15.220]\n    (NP [11.895] (PU *))))','*****')

def func(data):
    p1=re.compile(r'\s\[\d*?[.]\d*\]')
    return p1.sub('',data)

def fenju(data):
    return data.replace('(ROOT','+++\n(ROOT')
    
def sentlist(data):
    temp=data.split('*****')
    result=[]
    for sent in temp:
        sent = sent.strip()
        if sent !='':
            result.append(sent)
    return result

def cutlist(sent):
    temp=sent.split('+++')
    result=[]
    for cut in temp:
        cut=cut.strip()
        if cut !='':
            result.append(cut)
    return result
    
def hang(cut):
    p1=re.compile('\s+')
    result=p1.sub(' ',cut)
    result=result.strip()+'\n'
    return result
    
def combine_tree(list_tree):
    lenth=len(list_tree)
    root=ParseTree(list_tree[0])
    if root.generalized!='error':
        child_of_root=root.root['child']
        for _ in range(1,lenth):
            temp_root=ParseTree(list_tree[_])
            if temp_root.generalized!='error':
                child=temp_root.root['child']
                while child_of_root['brother']:
                    child_of_root=child_of_root['brother']
                root.generalized=root.generalized+'\t'+temp_root.generalized
                root.depth=max(root.depth,temp_root.depth)
                child_of_root['brother']=child
        root.update()
    else:
        print('error')
    return root


class ParseTree:
    def __init__(self, string):
        if string[0]=='(':
            temp=''
            stack=[]
            self.generalized = string.strip()
            self.depth=0
            #将广义表表示法转成孩子兄弟表示法存储
            self.root={'data':'ROOT','child':{},'brother':{}}
            sentences=self.generalized[5:]
            p=self.root
            stack.append(p)
            for item in sentences:
                if item == '(':
                    temp=''
                    stack.append(p)
                elif item == ' ':
                    if temp and not p['data']:
                        p['data']=temp
                        temp=''
                    r={'data':'','child':{},'brother':{}}
                    if p['child']!={}:
                        p['brother']=r
                    else:
                        p['child']=r
                    p=r
                elif item == ')':
                    if temp and not p['data']:
                        p['data']=temp
                        temp=''
                    p=stack.pop()
                    if p['child']:
                        while p['brother']!={}:
                            p=p['brother']
                else:
                    temp=temp+str(item)
            #求深度
            self._depth() 
            self._struct()
        else:
            self.generalized='error'
    
    def son(self,dic,a):
        a[:]=[]
        if dic['child']:
            a.append(dic['data'])
            son_list=[]
            temp=dic['child']
            son_list.append(temp)
            a.append(temp['data'])
            while temp['brother']:
                temp=temp['brother']
                son_list.append(temp)
                a.append(temp['data'])
            return son_list
        else:
            return None
            
    def _depth(self):
        queue_node = deque([])
        queue_level = deque([])
        son_struct=[]
        temp=[]
        max_level=0
        m=0
        root=self.root
        queue_node.append(root)
        queue_level.append(m)
        while(queue_node):
            node=queue_node.popleft()
            m=queue_level.popleft()
            son_struct=self.son(node,temp)
            if son_struct:
                m=m+1
                max_level=max(max_level,m)
                for item in son_struct:
                    queue_node.append(item)
                    queue_level.append(m)
        self.depth=max_level
                
    def _struct(self):
        self.struct_sent={}
        root=self.root
        son_struct=[]
        b=[]
        stack=[]
        stack.append(root)
        while stack:
            node=stack.pop()
            son_struct=self.son(node,b)
            if son_struct:
                if len(b)>2:
                    name=','.join(map(str,b))
                    self.struct_sent[name]=self.struct_sent.get(name,0)+1
                for item in son_struct:
                    stack.append(item)
                    
    def update(self):
        self._struct()
            

def most_n(n,path):
    filelist=os.listdir(path)
    dic_struct={}
    for file in filelist:
        infile=open(path+file,'r',encoding='utf-8')
        for line in infile:
            dic_line=json.loads(line)
            line_struct=dic_line['struct']
            for item in line_struct:
                dic_struct[item]=dic_struct.get(item,0)+line_struct[item]
        infile.close()
    list_sort=sorted(dic_struct.items(),key=lambda x:x[1],reverse=True)
    list_sort=list_sort[:n]
    result={}
    for _ in list_sort:
        result[_[0]]=_[1]
    return result

def file_info(filepath,feature):
    file=open(filepath,'r',encoding='utf-8')
    num_line=0
    sum_depth=0
    dic_file={}
    for line in file:
        num_line+=1
        dic_sent=json.loads(line)
        sum_depth+=dic_sent['depth']
        line_struct=dic_sent['struct']
        for item in line_struct:
            dic_file[item]=dic_file.get(item,0)+line_struct[item]
    if num_line:
        avg_depth=int(sum_depth/num_line)
    else:
        avg_depth=0
    sum_struct=len(dic_file)
    num=sum(dic_file.values())
    result=[]
    result.append(avg_depth)
    result.append(sum_struct)
    for f in feature:
        if num:
            result.append(dic_file.get(f,0)/num)
        else:
            result.append(0)
    file.close()
    return result
    
