import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os


# 获取网页
def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''


# 获取数据
def getDataInfo(infoList, url, pre_params, *args):
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

    for i in range(pages):  # 遍历每一页
        page = i + 1
        url = url + '&page=' + str(page)
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
    data = pd.DataFrame(infoList)
    # with open(r'./info.csv','w+',encoding='utf-8') as f:
    try:

        data.columns = ['标题', '学校', '门类/专业', '招生人数', '发布时间', '链接']
    except:
        print('没有调剂信息...')

    try:
        if not os.path.exists(path):
            data.to_csv(path)
            print('保存成功')
        else:
            print('路径存在')
    except:
        print('保存失败')


# 设定查询参数 -- 专业、年份
def parameters(pro_='', pro_1='', pro_2='', year=''):
    paramsList = [pro_, pro_1, pro_2, year]
    return paramsList


def main():
    url = 'http://muchong.com/bbs/kaoyan.php?'
    path = './data_info.csv'
    pre_params = ['r1%5B%5D=', 'r2%5B%5D=', 'r3%5B%5D=', 'year=']
    params = parameters(pro_='08', pro_1='0801')
    dataList = []
    getDataInfo(dataList, url, pre_params, *params)
    outputCSV(dataList, path)


main()
