#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-29 21:17:36
# @Author  : Kaiyan Zhang (kaiyanzh@outlook.com)
# @Link    : https://github.com/iseesaw
# @Version : v1.0
"""
将csdn博客导出为markdown
方法：
1. 编辑博客，抓包
2. 获取博客markdown格式链接
https://mp.csdn.net/mdeditor/getArticle?id=100125817
3. 模拟请求
Request Headers
:authority: mp.csdn.net
:method: GET
:path: /mdeditor/getArticle?id=100125817
:scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,zh-TW;q=0.8
cookie: uuid_tt_dd=10_7363320700-1563628438907-864526; dc_session_id=10_1563628438907.833516; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_7363320700-1563628438907-864526!5744*1*qq_36962569!1788*1*PC_VC; UN=qq_36962569; smidV2=20190712194742cdeda8c033ea9ef003a9a0003c79154a00358928f445b7b50; UserName=qq_36962569; UserInfo=3a33c991856940a79235b113cb42ff0d; UserToken=3a33c991856940a79235b113cb42ff0d; UserNick=%E5%AD%90%E8%80%B6; AU=5A5; BT=1566296770044; p_uid=U000000; TINGYUN_DATA=%7B%22id%22%3A%22-sf2Cni530g%23HL5wvli0FZI%22%2C%22n%22%3A%22WebAction%2FCI%2FpostList%252Flist%22%2C%22tid%22%3A%22e0a1148715d862%22%2C%22q%22%3A0%2C%22a%22%3A42%7D; ViewMode=list; aliyun_webUmidToken=T9204DD7B1A1971E571EFE43913410386D4C2C9D905BA336A2BEDBC206D; hasSub=true; c_adb=1; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1567074771,1567083797,1567083801,1567084099; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1567084279; dc_tos=px01z9
referer: https://mp.csdn.net/mdeditor/100125817
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: 
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36

Query String Parameters
id=100125817
"""
import json
import uuid
import time
import requests
import datetime
from bs4 import BeautifulSoup


def request_blog_list(page=1):
    """获取博客列表
    主要包括博客的id以及发表时间等
    """
    url = f'https://blog.csdn.net/qq_36962569/article/list/{page}'
    reply = requests.get(url)
    parse = BeautifulSoup(reply.content, "lxml")
    spans = parse.find_all('div', attrs={'class':'article-item-box csdn-tracking-statistics'})
    blogs = []
    for span in spans[:3]:
        try:
            href = span.find('a', attrs={'target':'_blank'})['href']
            read_num = span.find('span', attrs={'class':'num'}).get_text()
            date = span.find('span', attrs={'class':'date'}).get_text()
            blog_id = href.split("/")[-1]
            blogs.append([blog_id, date, read_num])
        except:
            print('Wrong, ' + href)
    return blogs

def request_md(blog_id, date):
    """获取博客包含markdown文本的json数据"""
    url = f"https://mp.csdn.net/mdeditor/getArticle?id={blog_id}"
    headers = {
        #"cookie": "uuid_tt_dd=10_7363320700-1563628438907-864526; dc_session_id=10_1563628438907.833516; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_7363320700-1563628438907-864526!5744*1*qq_36962569!1788*1*PC_VC; UN=qq_36962569; smidV2=20190712194742cdeda8c033ea9ef003a9a0003c79154a00358928f445b7b50; UserName=qq_36962569; UserInfo=3a33c991856940a79235b113cb42ff0d; UserToken=3a33c991856940a79235b113cb42ff0d; UserNick=%E5%AD%90%E8%80%B6; AU=5A5; BT=1566296770044; p_uid=U000000; TINGYUN_DATA=%7B%22id%22%3A%22-sf2Cni530g%23HL5wvli0FZI%22%2C%22n%22%3A%22WebAction%2FCI%2FpostList%252Flist%22%2C%22tid%22%3A%22e0a1148715d862%22%2C%22q%22%3A0%2C%22a%22%3A42%7D; ViewMode=list; aliyun_webUmidToken=T9204DD7B1A1971E571EFE43913410386D4C2C9D905BA336A2BEDBC206D; hasSub=true; c_adb=1; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1567074771,1567083797,1567083801,1567084099; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1567084279; dc_tos=px01z9",
        #"cookie": "uuid_tt_dd=10_7363320700-1563628438907-864526; dc_session_id=10_1563628438907.833516; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_7363320700-1563628438907-864526!5744*1*qq_36962569!1788*1*PC_VC; UN=qq_36962569; smidV2=20190712194742cdeda8c033ea9ef003a9a0003c79154a00358928f445b7b50; UserName=qq_36962569; UserInfo=3a33c991856940a79235b113cb42ff0d; UserToken=3a33c991856940a79235b113cb42ff0d; UserNick=%E5%AD%90%E8%80%B6; AU=5A5; BT=1566296770044; p_uid=U000000; hasSub=true; c_adb=1; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1567171221,1567173255,1567173925,1567173939; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1567174790; dc_tos=px1ztc",
        "cookie": "uuid_tt_dd=10_7363320700-1563628438907-864526; dc_session_id=10_1563628438907.833516; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_7363320700-1563628438907-864526!5744*1*qq_36962569!1788*1*PC_VC; UN=qq_36962569; smidV2=20190712194742cdeda8c033ea9ef003a9a0003c79154a00358928f445b7b50; UserName=qq_36962569; UserInfo=3a33c991856940a79235b113cb42ff0d; UserToken=3a33c991856940a79235b113cb42ff0d; UserNick=%E5%AD%90%E8%80%B6; AU=5A5; BT=1566296770044; p_uid=U000000; hasSub=true; c_adb=1; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1567171221,1567173255,1567173925,1567173939; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1567174790; dc_tos=px1zy1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36"
    }
    data = {"id": blog_id}
    reply = requests.get(url, headers=headers, data=data)

    try:
        write_hexo_md(reply.json(), date)
    except Exception as e:
        print("***********************************")
        print(e)
        print(url)
        #print(reply.json())

def write_hexo_md(data, date):
    """将获取的json数据解析为hexo的markdown格式"""
    title = data["data"]["title"]
    title = title.replace("[", "【")
    title = title.replace("]", "】")
    tags = data["data"]["tags"]
    # 页面唯一标识符，用于统计系统和评论系统
    key = "key" + str(uuid.uuid4())

    name = f"{date[0]}-{date[1]}-{date[2]}-{title}"
    tag = "tags:\n    - " + "\n    - ".join(tags.split(","))
    header = "---\n" + f"title: {title}\n" + tag + "\n" + f"key: {key}\n" + "---\n\n"

    content = data["data"]["markdowncontent"].replace("@[toc]", "")

    with open(f"blogs/{name}.md", "w", encoding="utf-8") as f:
        f.write(header + content)

    print(f"写入 {name}")


def main(total_pages=3):
    """
    获取博客列表，包括id，时间
    获取博客markdown数据
    保存hexo格式markdown
    """
    blogs = []
    for page in range(1, total_pages + 1):
        blogs.extend(request_blog_list(page))
    for blog in blogs:
        blog_id = blog[0]
        date = blog[1].split(" ")[0].split("-")
        request_md(blog_id, date)
        time.sleep(1)

if __name__ == '__main__':
    main()