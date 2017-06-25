# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 19:35:26 2017

@author: DaCapo
"""

import os
from xml.dom.minidom import parse
import xml.etree.ElementTree as ET
import pickle
import ace_filereader as fr

#获取文档（弃用）
def getText():
    filename = []
    data=[]
    for root, dirs, files in os.walk("Chinese"):
        for fn in files:
            root_arr = root.split("\\")
            X = ""
            if(fn.find(".sgm")>0 and root.find("\\adj")>0):
                doc = parse(root+"\\"+fn)
                if(root_arr[1]=="wl"):
                    for turn in doc.getElementsByTagName('POST'):
                       X += turn.childNodes[-1].data.replace("\n","").replace(" ","")
                    data.append(X)
                    filename.append(fn)
                elif(root_arr[1]=="nw"):
                    for turn in doc.getElementsByTagName('TEXT'):
                       X += turn.childNodes[-1].data.replace("\n","").replace(" ","")
                    data.append(X)
                    filename.append(fn)
                    
                else:
                    for turn in doc.getElementsByTagName('TURN'):
                       X += turn.childNodes[-1].data.replace("\n","").replace(" ","")
                    data.append(X)
                    filename.append(fn)
                assert(X!="")
    return dict(zip(filename, data))

#遍历文件获取所有的实体 关系 文档
def get_ERDs():
    E = {}
    R = {}
    D = {}
    for root, dirs, files in os.walk("Chinese"):
        for fn in files:
#            root_arr = root.split("\\")
#            fn_arr = fn.split(".")
            if(fn.find(".sgm")>0 and root.find("\\adj")>0):
                f_no = fn[0:-4]
                named_entities, rels, doc = fr.get_ERD(root+"\\"+f_no)
                E[f_no]=named_entities
                R[f_no]=rels
                D[f_no]=doc
    return E, R , D

#导入ace的数据
def load():
    #判断是否需要创建文件
    if not os.path.exists(r'nes_res.pkl'):
        create()
    #读取文件  
    with open('nes_res.pkl', 'rb') as f:
        data = pickle.load(f)
        
    return data

#创建 实体 关系 文档的数据文件
def create():
    nes, res, docs = get_ERDs()
#    texts = getText()
    
    with open('nes_res.pkl', 'wb') as output:
        pickle.dump({"nes":nes,"res":res, "docs":docs}, output)

def conbime_list_dic(ld):
    return dict(pair for d in ld for pair in d.items())


if __name__ == "__main__":
    datatest = load()
    
#     for x in rl:
#        if x =="METONYMY":
#            print x