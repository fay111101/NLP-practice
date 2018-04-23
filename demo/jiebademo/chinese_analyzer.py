#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Time    : 18-4-23 下午2:14
@Author  : fay
@Email   : fay625@sina.cn
@File    : chinese_analyzer.py
@Software: PyCharm
"""
from __future__ import unicode_literals
import sys, os

sys.path.append("../")
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
import jieba.analyse as analyse

analyzer = analyse.ChineseAnalyzer()
schema = Schema(title=TEXT(stored=True), path=ID(stored=True),
                content=TEXT(stored=True, analyzer=analyzer))

if not os.path.exists("tmp"):
    os.mkdir("tmp")

ix = create_in("tmp", schema)  # for create new index
# ix = open_dir("tmp") # for read only
writer = ix.writer()

writer.add_document(
    title="document1",
    path="/a",
    content="This is the first document we’ve added!"
)

writer.add_document(
    title="document2",
    path="/b",
    content="The second one 你 中文测试中文 is even more interesting! 吃水果"
)

writer.add_document(
    title="document3",
    path="/c",
    content="买水果然后来世博园。"
)

writer.add_document(
    title="document4",
    path="/c",
    content="工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作"
)

writer.add_document(
    title="document4",
    path="/c",
    content="咱俩交换一下吧。"
)

writer.commit()
searcher = ix.searcher()
parser = QueryParser("content", schema=ix.schema)

for keyword in ("水果世博园", "你", "first", "中文", "交换机", "交换"):
    print(keyword + "的结果为如下：")
    q = parser.parse(keyword)
    results = searcher.search(q)
    for hit in results:
        print(hit.highlights("content"))
    print("\n--------------我是神奇的分割线--------------\n")

for t in analyzer(
        "我的好朋友是李明;我爱北京天安门;IBM和Microsoft; I have a dream. this is intetesting and interested me a lot"):
    print(t.text)