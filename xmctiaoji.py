# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
from threading import Thread
from threading import Lock
import time


def getHTMLText(url):
    """
    获取网页
    """
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''


def getPages(infoList, url, pre_params, *args):
    """
    获取当前需要爬取的页面数，及完整链接
    """

    params = []
    count = -1
    for i in args:
        count += 1
        par_ = pre_params[count] + i
        params.append(par_)

    for param in params:
        url += param + '&'

    # print(url)
    html = getHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')

    # 处理空页异常
    try:
        pages_tag = soup.find_all('td', 'header')[1].string
        pages = int(re.split('/', pages_tag)[1])
    except:
        pages = 0

    # 判读是否只有一页
    if pages == 0:
        pages += 1

    return pages, url


page = 0
lock = Lock()


def getDataInfo(infoList, pages, url):
    """
    获取数据信息
    """
    global page
    while True:
        lock.acquire()
        page += 1
        lock.release()
        if page > pages:
            break
        url = url + '&page=' + str(page)
        time.sleep(1)
        # lock.acquire()
        html = getHTMLText(url)
        soup = BeautifulSoup(html, 'html.parser')
        tbody = soup.find_all('tbody', 'forum_body_manage')[0]
        trs = tbody.find_all('tr')  # 每个学校的全部信息被tr标签包围
        for tr in trs:  # 遍历每一个学校
            dicts = {}
            href = tr.find_all('a')[0].get('href')  # 定位至a标签，提取href的属性值
            tds = tr.find_all('td')  # 每个学校的各个信息包含在td标签内
            lens = len(tds)
            for i in range(lens):
                if i == 0:
                    title = tds[i].find('a').string
                    dicts[i] = title
                else:
                    dicts[i] = tds[i].string
            dicts['href'] = href
            print(dicts)
            infoList.append(dicts)


def outputCSV(infoList, path):
    """
    输出文档
    """
    data = pd.DataFrame(infoList)
    try:

        data.columns = ['标题', '学校', '门类/专业', '招生人数', '发布时间', '链接']
        data.sort_values(by='发布时间', ascending=False, inplace=True)
        data = data.reset_index(drop=True)
    except:
        print('没有调剂信息...')
        return

    try:
        if not os.path.exists(path):
            data.to_csv(path)
            print('爬取成功')
        else:
            print('路径存在')
    except:
        print('保存失败')


def parameters(pro_='', pro_1='', pro_2='', year=''):
    """
    设定查询参数 -- 专业、年份
    """
    paramsList = [pro_, pro_1, pro_2, year]
    return paramsList


def threadingUp(count, infoList, pages, url):
    """
    启动多线程
    """
    threadList = []
    iList = []
    for i in range(count):
        iList.append(i)
        t = Thread(target=getDataInfo, args=(infoList, pages, url))
        t.start()
        threadList.append(t)
    for thread in threadList:
        thread.join()


def main():
    url = 'http://muchong.com/bbs/kaoyan.php?'
    path = './08_0812.csv'
    pre_params = ['r1%5B%5D=',  'r2%5B%5D=', 'r3%5B%5D=', 'year=']
    params = parameters(pro_='08', pro_1='0812',year='2020')
    dataList = []
    count = 1000
    pages, url_ = getPages(dataList, url, pre_params, *params)
    start = time.time()
    threadingUp(count, dataList, pages, url_)  # 多线程
    # getDataInfo(dataList,pages,url_) # 单线程
    outputCSV(dataList, path)
    end = time.time()
    print('时间:'+str(end - start))


if __name__ == "__main__":
    main()
