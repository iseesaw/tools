#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-31 16:21:59
# @Author  : Kaiyan Zhang (kaiyanzh@outlook.com)
# @Link    : https://github.com/iseesaw
# @Version : $Id$

import os
import requests
from bs4 import BeautifulSoup


def get_search_result(keyword):
    url = f"https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q={keyword}&btnG="
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"

        #"Cookie": NID=188=d66lexgk1weNuRBKiYQa-dTwfLlMD91ix9rUUzi-hBA11IqRLHw6D9vGCN4m_Xr9KEvr5pz19tGbH363_a5mOv3WpIsn5aI49CR6c-O0TUPiMkW2W_T9E7A2_hmin0vfvnZ3dsuCo7tILsQ104NpB_VTBAN9ri5koXK10b75oLVTAJU9-HTzA_qEnnOFuKB4tR36MJG6UoerZCEA; SID=YAc8JzWOoJ9qfqhacLhJV0mMtMcnvwnuyXRwBQqda2ix-zM9zJcs6LkPQqLXE-OiUz9PcA.; HSID=A1YkZvCNtV0Od0OlS; SSID=AhIvcOb2Dem2Iq1VE; APISID=G-zoJZFZIea5DWT4/AtjVL3_TMA4E-qLwJ; SAPISID=LTtQsWIPUIBjRZZ3/AbGMK8cke1M9bKCaO; ANID=AHWqTUl3Zna_xXlxRmtsCv3HxVJLGZCrtjgEI2WGthzANSAkHmRfHmsWgmLT_aYu; 1P_JAR=2019-08-31-08; GSP=LM=1567233827:S=36fKNlEqU7dwOK3G
    }

    reply = requests.get(url, headers=headers)
    parser = BeautifulSoup(reply.content, "lxml")

    article = parser.find("div", attrs={"class": "gs_r gs_or gs_scl"})
    cid = article["data-cid"]

    name = parser.find("a", attrs={"id": cid})
    title = name.get_text()

    result = {
        "title": title,
        "cites": get_citation(cid)
    }

    return result


def get_citation(cid):
    url = f"https://scholar.google.com/scholar?q=info:{cid}:scholar.google.com/&output=cite&scirp=0&hl=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }

    reply = requests.get(url, headers=headers)
    parser = BeautifulSoup(reply.content, "lxml")

    ths = parser.find_all("th", attrs={"class": "gs_cith"})
    trs = parser.find_all("div", attrs={"class": "gs_citr"})
    print(ths, trs)
    cites = []
    for th, tr in zip(ths, trs):
        cites.append({"name":th.get_text(), "body":tr.get_text()})

    return cites