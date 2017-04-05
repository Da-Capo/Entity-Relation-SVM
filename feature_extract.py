# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 10:30:53 2017

@author: DaCapo
"""

import ace_data
import jieba
import numpy as np
import re
from nltk.tokenize.stanford_segmenter import StanfordSegmenter
import jieba.posseg as pseg 
import token



#词性对应表list
#POS = u"eng	Mg	Rg	a	ad	ag	al	an	b	begin	bl	c	cc	d	dg	dl	e	end	f	gb	gc	gg	gi	gm	gp	i	j	k	l	m	mq	n	nba	nbc	nf	ng	nhd	nhm	nis	nit	nmc	nnd	nnt	nr	nr1	nr2	nrf	nrj	ns	nsf	nt	ntc	ntcb	ntcf	ntch	nth	nto	nts	ntu	nz	o	p	pba	pbei	q	qt	qv	r	rr	ry	rys	ryt	ryv	rz	rzs	rzt	rzv	s	t	tg	u	ude1	ude2	ude3	udeng	udh	uguo	ule	ulian	uls	usuo	uyy	uzhe	uzhi	v	vd	vf	vg	vi	vl	vn	vshi	vx	vyou	w	x	y	z"
POS = u"eng a ad ag an b c d df dg e f g h i j k l m mg mq n ng nr nrfg nrt ns nt nz o p q r rg rr rz s t tg u ud ug uj ul uv uz v vd vg vi vn vq x y z zg"
POS = POS.split(" ")

#获取一个词的词袋对应数字
def get_token(s, tokens):
    return tokens.index(s)+1 if s in tokens else 0

#对文档s分词
def get_seg(docs):
    cut_result={}
    for f_no in docs: 
        doc = docs[f_no]
        st = []
        cutw = []
        offset=0
        words = pseg.cut(doc)
        for word, flag in words:
            if not word == " ":
                st.append(offset)
                cutw.append((word,POS.index(flag)))
            offset += len(word)
        cut_result[f_no] = [st,cutw]
    return cut_result

#导入数据
data = ace_data.load()
docs = data["docs"]
nes = data["nes"]
res = data["res"]

#导入词袋
tokens = token.get_tokens()

#文本分词
seg_docs =  get_seg(docs)

#获取各种的类型对应表list
el = sorted(list(set([x[1] for f in nes.values() for x in f.values()])))
esl= sorted(list(set([x[-1] for f in nes.values() for x in f.values()])))
rl= sorted(list(set([x[1] for f in res.values() for x in f.values()])))
rsl= sorted(list(set([x[2] for f in res.values() for x in f.values()])))

#提取特征过程
w = 2
features = {}
lables = {}
for f_no in res:
    sts = seg_docs[f_no][0]
    words = seg_docs[f_no][1]     
    for r_no in res[f_no]:
        e1 = nes[f_no][res[f_no][r_no][4]]
        e2 = nes[f_no][res[f_no][r_no][5]]
        st1 = e1[2]
        ed1 = e1[3]
        st2 = e2[2]
        ed2 = e2[3]
        sidx1 = sts.index(st1)
        eidx1 = sidx1
        while sts[eidx1+1] < ed1:
            eidx1 += 1
        sidx2 = sts.index(st2)
        eidx2 = sidx2
        while sts[eidx2+1] < ed2:
            eidx2 += 1
            
        #判断包含关系
        if res[f_no][r_no][6][1] <= res[f_no][r_no][7][0]:
            order = 0 
        elif res[f_no][r_no][7][1] <= res[f_no][r_no][6][0]:
            order = 1
        else: 
            order = 2
            
        #特征组合
        feature= [el.index(e1[1]), el.index(e2[1]), esl.index(e1[-1]), esl.index(e2[-1]), order]
        e1_w, e1_t, e2_w, e2_t = [],[],[],[]
        for i in range(w):
            e1_w.insert(0,get_token(words[sidx1-i][0],tokens))
            e1_w.append(get_token(words[sidx1+i][0],tokens))
            e1_t.insert(0,words[sidx1-i][1])
            e1_t.append(words[eidx1+i][1])
            e2_w.insert(0,get_token(words[sidx2-i][0],tokens))
            e2_w.append(get_token(words[sidx2+i][0],tokens))
            e2_t.insert(0,words[sidx2-i][1])
            e2_t.append(words[eidx2+i][1])
            
        feature.extend(e1_w)
        feature.extend(e1_t)
        feature.extend(e2_w)
        feature.extend(e2_t)
        
        features[r_no] = (feature, rl.index(res[f_no][r_no][1]), rsl.index(res[f_no][r_no][2]))

#特征结果保存
with open('feature.pkl', 'wb') as output:
    out_data = {"features":features, 
                "POS":POS,"el":el,"esl":esl,"rl":rl,"rsl":rsl,
                "tokens":tokens }
    pickle.dump(out_data, output)
 
        