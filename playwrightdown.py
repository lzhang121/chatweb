# -*- coding: utf-8 -*-
# @Time : 2024/08/27 19:00
# @Author : zhanglei
# @Email : zhanglei@bonree.com
import requests
import time
from playwright.sync_api import sync_playwright

def download(prepath, song):
    with sync_playwright() as p:
        #browser = p.chromium.launch(headless=False)
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        #访问网页
        retries = 1
        max_retries = 5
        while retries <= max_retries:
            try:
                page.goto(song)
            except:
                time.sleep(1)
                retries += 1
                continue
            break
        #等待数据加载完成
        page.wait_for_load_state("load")
        #获取内容数量
        elements = page.query_selector_all('mp-common-mpaudio')
        if len(elements) != 0:
            download_urls = []
            for element in elements:
                content_count_element = element.get_attribute("voice_encode_fileid")
                if content_count_element:
                    download_url = 'https://res.wx.qq.com/voice/getvoice?mediaid=' + content_count_element
                    download_urls.append(download_url)
        else:
            browser.close()
            return

        prename = page.query_selector('.rich_media_title').text_content().strip().replace('\n', '').replace('\t', '')
        content_count_elements = page.query_selector_all('.rich_media_content p')
        if len(content_count_elements) <= 10:
             content_count_elements = page.query_selector_all('.rich_media_content span')

        page_text = []
        for content in content_count_elements:
            page_text.append(content.text_content().replace(u'\xa0', u''))

        name = prepath + '/'+ prename
        download_audio(download_urls,name)
        print("download {} audio done".format(name))
        download_text(page_text, name)
        print("download {} text done".format(name))

        # 图片
        elements = page.query_selector_all('.rich_pages')
        urls = []
        for element in elements:
            url = element.get_attribute('data-src')
            if url is not None and 'mmbiz.qpic.cn' in url:
                urls.append(url)
        if len(urls):
            download_img(urls, name)

        browser.close()

def download_audio(urls, name):
    for index in range(len(urls)):
        res = requests.get(urls[index])
        music = res.content
        if len(urls) == 1:
            file_name = name + '.mp3'
        else:
            file_name = name + str(index) + '.mp3'
        with open(file_name, 'ab') as file:
            file.write(res.content)
            file.flush()

def download_text(content, name):
    file_name = name + '.txt'
    with open(file_name, 'w') as f:
        f.write('\n'.join(content))

def download_img(urls, name):
    for index in range(len(urls)):
        if index == 0:
            continue
        res = requests.get(urls[index])
        img = res.content
        if len(urls) == 2:
            file_name = name + '.jpeg'
        else:
            file_name = name + str(index) + '.jpeg'
        with open(file_name, 'wb') as f:
            f.write(img)


if __name__ == "__main__":
    prepath = '中译日赞美诗'
    #song = 'https://mp.weixin.qq.com/s?__biz=MjM5Nzc1Nzc5OA==&mid=2648657294&idx=2&sn=29083680e8815f137637f17d8b524947&chksm=befefb8789897291057d1d5200c17164ddb4f2764372f90d8cca3f81bdcba9d07719bce77dbf&scene=178&cur_album_id=1351391417389907972#rd'
    song = 'https://mp.weixin.qq.com/s?__biz=MjM5Nzc1Nzc5OA==&mid=2648657754&idx=1&sn=fa1a11a5a397853ea2d3d296344b5880&chksm=befef9538989704536238b6263e50017962fa786dac7b8369d72e3e34ae6f09684be7eca80c0&scene=178&cur_album_id=1351391417389907972#rd'
    song = 'https://mp.weixin.qq.com/s?__biz=MjM5Nzc1Nzc5OA==&mid=2648657321&idx=2&sn=42ac92ae93526f2f400919d47947fff3&chksm=befefba0898972b68a83a01313f2c79cef24e513ce477f6e40a9d3a715505a1f19c900fca71c&scene=178&cur_album_id=2546974342422003712#rd'
    song = 'https://mp.weixin.qq.com/s?__biz=MjM5Nzc1Nzc5OA==&mid=2648657754&idx=1&sn=fa1a11a5a397853ea2d3d296344b5880&chksm=befef9538989704536238b6263e50017962fa786dac7b8369d72e3e34ae6f09684be7eca80c0&scene=178&cur_album_id=1351391417389907972#rd'
    #song = 'https://mp.weixin.qq.com/s?__biz=MjM5Nzc1Nzc5OA==&mid=2648657321&idx=2&sn=42ac92ae93526f2f400919d47947fff3&chksm=befefba0898972b68a83a01313f2c79cef24e513ce477f6e40a9d3a715505a1f19c900fca71c&scene=178&cur_album_id=2546974342422003712#rd'
    song = 'https://mp.weixin.qq.com/s?__biz=MjM5Nzc1Nzc5OA==&mid=2648657581&idx=1&sn=0b7aa8f078ecada701e09a1d2260c1c2&chksm=befef8a4898971b2d4ae5cc327f8cb55685d0297c4abfb67c7c485a26d59235afa8735d14299&scene=178&cur_album_id=1351391417389907972#rd'
    song = 'https://mp.weixin.qq.com/s?__biz=MjM5Nzc1Nzc5OA==&mid=2648657642&idx=3&sn=6f4c2a280547107ef338ff8090242a33&chksm=befef8e3898971f59bb0c83921c2ef7d5bedc47fce03d9c642ff5ed5104b13a6f21270d756ae&scene=178&cur_album_id=1409526905740820481#rd'

    download(prepath, song)
