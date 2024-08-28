# -*- coding: utf-8 -*-
# @Time : 2024/08/27 11:19
# @Author : zhanglei
# @Email : zhanglei@bonree.com

import re
import time
from playwright.sync_api import sync_playwright
def slide(album):
    with sync_playwright() as p:
        #browser = p.chromium.launch(headless=False)
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        #访问网页
        url = "https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MjM5Nzc1Nzc5OA==&action=getalbum&album_id=" + album
        retries = 1
        max_retries = 5
        while retries <= max_retries:
            try:
                page.goto(url)
            except:
                time.sleep(1)
                retries += 1
                continue
            break

        #等待数据加载完成
        page.wait_for_load_state("load")
        #获取内容数量
        content_count_element = page.query_selector('.album__desc-content.js_album_desc_content > span')
        content_count_text = content_count_element.inner_text()
        content_count = int(re.search(r'\d+', content_count_text).group()) // 10
        #滑动页面
        for _ in range(content_count):
            print("第"+str(_+1)+"次滑动.....")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)

        #获取标题
        list_items = page.query_selector_all(".album__list.js_album_list > .album__list-item")
        #输出标题和链接
        songs = []
        for item in list_items:
            data_link = item.get_attribute("data-link")
            songs.append(data_link)
        browser.close()
    time.sleep(2)
    return songs

if __name__ == "__main__":
    album = '1420951930242957312'
    slide(album)
