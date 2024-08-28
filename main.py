# -*- coding: utf-8 -*-
# @Time : 2024/08/26 23:05
# @Author : zhanglei
# @Email : zhanglei@bonree.com
import requests
import os
import time
from lxml import etree
from playwrightslipe import slide
from playwrightdown import download

def download_album(album):
    base_url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5Nzc1Nzc5OA==&action=getalbum&album_id="
    url = base_url + album
    payload = {}
    headers = {'Cookie': 'rewardsn=; wxtokenkey=777'}
    response = requests.request("GET", url, headers=headers, data=payload)
    root = etree.HTML(response.text)
    album_name = root.xpath('//*[@id="js_tag_name"]/text()')
    prepath = album_name[0]
    isExists = os.path.exists(prepath)
    if not isExists:
        os.makedirs(prepath)
    songs = slide(album)
    time.sleep(2)
    for song in songs:
        download(prepath, song)

if __name__ == "__main__":
    albums = ['1351391417389907972','2729654071594647553','1420951930242957312','2792532868173725699','2546974342422003712']
    #albums = ['1351391417389907972']
    for album in albums:
        download_album(album)

