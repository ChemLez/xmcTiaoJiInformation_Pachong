# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
from threading import Thread
from threading import Lock


class GetXmcInfo(object):

    _url = 'http://muchong.com/bbs/kaoyan.php?'
    _page = 0
    _count = 1000
    _lock = Lock()
    _datalist = []

    def __init__(self, pro_='', pro_1='', pro_2='', year=''):
        self.pro_ = str(pro_)
        self.pro_1 = str(pro_1)
        self.pro_2 = str(pro_2)
        self.year = str(year)
        pass

    def __getHTMLText(self, url):
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

    def __getPages(self, url, pre_params, *args):
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
        html = GetXmcInfo.__getHTMLText(self, url)
        soup = BeautifulSoup(html, 'html.parser')

        # 处理空页异常
        try:
            pages_tag = soup.find_all('td', 'header')[1].string
            pages = int(re.split('/', pages_tag)[1])
        except:
            pages = 1

        return pages, url

    def __getDataInfo(self, infoList, pages, url):
        """
        获取数据信息
        """
        while True:
            try:
                GetXmcInfo._lock.acquire()
                GetXmcInfo._page += 1
                GetXmcInfo._lock.release()
                if GetXmcInfo._page > pages:
                    break
                url = url + '&page=' + str(GetXmcInfo._page)
                time.sleep(1)
                # lock.acquire()
                html = GetXmcInfo.__getHTMLText(self, url)
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
            except:
                print('')

    def __outputCSV(self, infoList, path):
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

    def __threadingUp(self, infoList, pages, url):
        """
        启动多线程
        """
        threadList = []
        iList = []
        for i in range(GetXmcInfo._count):
            iList.append(i)
            t = Thread(target=GetXmcInfo.__getDataInfo,
                       args=(self, infoList, pages, url))
            t.start()
            threadList.append(t)
        for thread in threadList:
            thread.join()

    def startUp(self, path='./information.csv'):
        pre_params = ['r1%5B%5D=',  'r2%5B%5D=', 'r3%5B%5D=', 'year=']
        params = (self.pro_, self.pro_1, self.pro_2, self.year)
        pages, url_ = GetXmcInfo.__getPages(
            self, GetXmcInfo._url, pre_params, *params)
        start = time.time()
        GetXmcInfo.__threadingUp(
            self, GetXmcInfo._datalist, pages, url_)  # 多线程
        # getDataInfo(dataList,pages,url_) # 单线程
        GetXmcInfo.__outputCSV(self, GetXmcInfo._datalist, path)
        end = time.time()
        print('时间:'+str(end - start))


print('提示:可查询内容有学科门类、一级学科、二级学科、年份，皆为选填,若不填直接回车\n保存路径的文件为CSV格式,例如:/information.csv\n附:小木虫官网:http://muchong.com/bbs/kaoyan.php')
pro_0 = input('请输入查询学科门类代码:')
pro_1_1 = input('请输入一级学科代码:')
pro_2_2 = input('请输入二级学科代码:')
pro_year = input('请输入查询年份:')
pro_path = input('保存路径:')
exampel = GetXmcInfo(pro_=pro_0, pro_1=pro_1_1, pro_2=pro_2_2, year=pro_year)
exampel.startUp(pro_path)
