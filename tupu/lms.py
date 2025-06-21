# -*- coding: UTF-8 -*-
# coding=utf-8  # 注意等号两侧无空格
# -*-coding:GBK-*-
import os
import sys

from langchain_community.graphs import Neo4jGraph

import llm

sys.path.append("/home/ubuntu/Python")

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)

# llm = loadLLM("OpenAI")

# llm = loadLLM("Xunfei")
# llm = loadLLM("Tengxun")
# llm = loadLLM("Ali")
