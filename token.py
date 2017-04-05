# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 17:04:58 2017

@author: DaCapo
"""

#categories = ['alt.atheism', 'soc.religion.christian',
#              'comp.graphics', 'sci.med']

#from sklearn.datasets import fetch_20newsgroups
#twenty_train = fetch_20newsgroups(subset='train',
#    categories=categories, shuffle=True, random_state=42)


import ace_data
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
import jieba
import numpy as np
import re

def has_chinese(s):
    """判断一个unicode是否是汉字"""
    return re.match(ur"[\u4e00-\u9fa5]",s)
 
def has_number(s):
    """判断一个unicode是否是数字"""
    return re.match(ur"[\u0030-\u0039]",s)
 
def has_alphabet(s):
    """判断一个unicode是否是英文字母"""
    return re.match(ur"[\u0041-\u005a]",s) or re.match(ur"[\u0061-\u007a]",s)

def checklist(l, callback):
    return [ x for x in l if callback(x[4])]


#建立词袋
def get_tokens():
    vectorizer = CountVectorizer()
#    global data, cut_docs
    data = ace_data.load()
    docs = data["docs"]
    cut_docs = []
    BOW_data = []
    #nes = erdata.conbime_list_dic(data["nes"].values())
#    xxx =[ x for x in nes.values() if has_number(x[4])]
    nes = data["nes"]
    
    print  "载入字典"
    #for ne in nes:
    #    jieba.add_word(ne[4])
    #    BOW_data += ne[4]+" "
        
    print  "开始分词"
    #分词
    for k in docs:
        result = ' '.join(jieba.cut(docs[k]))
        cut_docs.append(result)
        this_nes = [x[1][4] for x in nes[k].items()]
        BOW_data.append(result+" "+" ".join(this_nes))
        
    print "创建词袋"
    X_train_counts = vectorizer.fit_transform(cut_docs)
    print X_train_counts.shape
    
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    X_train_tfidf.shape
    tf = np.sum(X_train_counts.A, axis=0)
    tokens = vectorizer.get_feature_names()
    tf_dict = {}
    for i in range(len(tokens)):
        if not has_number(tokens[i]):
            tf_dict[tokens[i]] = tf[i]
            
    dict_sorted = sorted(tf_dict.iteritems(), key=lambda d:d[1], reverse=True)
    tf_tokens = [key for key,value in dict_sorted][:20000]

    return tf_tokens

if __name__ == "__main__":
    tokens = get_tokens()
    print get_token(u"66", tokens)

