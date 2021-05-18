#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import pypinyin              # 与xpinyin相比，pypinyin更强大。
import time
from pyecharts.globals import ThemeType
from pyecharts import options as opts
from pyecharts.charts import Bar

# 爬虫目标地址：http://www.gaokao.com/jiangsu/fsx/

# 有反爬，添加一下header
headers = {
    'User - Agent': 'Mozilla / 5.0(Windows NT 6.1;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 73.0.3683.103Safari / 537.36'
}

# 爬虫请求
def yanz(diquname):
    diquPY = ''
    for i in pypinyin.pinyin(diquname, style=pypinyin.NORMAL):
        diquPY += ''.join(i)
    #print('汉字转拼音：',diquPY)
    url = 'http://www.gaokao.com/' + diquPY + '/fsx/'
    print(url)
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        response.encoding = 'GBK'
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        # # 地区只要a标签的href属性
        # diqu = soup.find(class_='area_box')
        # zzr = diqu.find_all('a')
        # for item in zzr:
        #     diquname = item.text
        #     # diquhref = item.get('href')
        #     print(diquname)
        print('正在查询历年分数线：')
        getScore(soup)
        # wenke, nianfen = wenkechax(soup)  # 文科查询
        # like = likechax(soup)  # 理科查询
        # keshihua(diquname,like,wenke,nianfen)
        # return wenke,like
    else:
        print('输入地区错误或请求失败：', response.status_code)
        html = None
    return None


def getScore(soup):
    titles = soup.findAll(name='h3', attrs={'class': "blue"})
    tables = soup.findAll('table')
    res = []
    for index in range(len(titles)):
        obj = {}
        obj['type'] = titles[index].text
        table = tables[index]
        score = []
        for tr in table.findAll('tr'):
            for th in tr.findAll('th'): # 年份
                if th.text !='':
                    #print(th.text)
                    obj[th.text] = {}
            for td in tr.findAll("td"): # 分数
                tdNum = (td.text).strip()               # str对象-除去不规则符号\r\n\t\t\t\t,不除也可以。
                score.append(tdNum)
                obj[th.text]['score'] = score
        res.append(obj)
    print(res)

        


# 文科
def wenkechax(soup):
    wenke=[]
    nianfen =[]
    # div1 = soup.select('body > div.wrapper.tp10 > div.widbox690.lt > div.cjArea.tm15')
    # h2 = soup.select('div.cjArea.tm15 > h2 > a')[0].text
    # h3 = soup.select('div.cjArea.tm15 > h3 ')[0].text
    # print(h3)

    # table
    tables = soup.findAll('table')
    tab = tables[1]   # 要第一个table
    for tr in tab.findAll('tr'):
        for th in tr.findAll('th'): # 年份
            if th.text !='':
                #print(th.text)
                nianfen.append(th.text)
        for td in tr.findAll("td"): # 分数
            tdNum = (td.text).strip()               # str对象-除去不规则符号\r\n\t\t\t\t,不除也可以。
            #print(tdNum)               # 所有的批次都获取到了。
            wenke.append(tdNum)
    #print(wenke,type(wenke),len(wenke))
    # 为了好看，只要一二本数据。
    print('年份',nianfen)
    print('文科',wenke[:12])
    print('文科',wenke[12:24])
    return wenke,nianfen

# 理科
def likechax(soup):
    like = []         # 理科
    nianfen = []       # 年份
    # h4 = soup.select('div.cjArea.tm15 > h3.blue.ft14.txtC.lkTit ')[0].text
    # print(h4)
    # table
    tables = soup.findAll('table')
    tab = tables[2]   # 要第二个table
    for tr in tab.findAll('tr'):
        for th in tr.findAll('th'):  # 年份
            if th.text !='':
                #print(th.text)
                nianfen.append(th.text)
        for td in tr.findAll('td'):  # 分数
            #print(td.text)
            tdNum = (td.text).strip()               # str对象-除去不规则符号\r\n\t\t\t\t,不除也可以。
            like.append(tdNum)
    # 为了好看，只要一二本数据。
    print('年份', nianfen)
    print('理科', like[:12])
    print('理科', like[12:24])
    return like

# 历年高考录取分数线绘图
def keshihua(diquname,like,wenke,nianfen):
    print(like)
    # 为了好看，只要一二本数据。
    wenkeYb = wenke[:12]
    wenkeEb = wenke[12:24]
    likeYb = like[:12]
    likeEb = like[12:24]

    # 绘图
    c = Bar(init_opts=opts.InitOpts(theme=ThemeType.SHINE))
    c.add_xaxis([list(z) for z in zip(nianfen)])          # 年份-记住怎么读取出来的！

    c.add_yaxis('文科一本',[wenkeYb[i] for i in range(1,len(wenkeYb))])  # 去掉'一本'
    c.add_yaxis('理科一本', [likeYb[i] for i in range(1,len(likeYb))])
    c.add_yaxis('文科二本', [wenkeEb[i] for i in range(1,len(wenkeEb))])
    c.add_yaxis('理科二本',[likeEb[i] for i in range(1,len(likeEb))])
    c.set_global_opts(title_opts=opts.TitleOpts(title=diquname +'历年高考录取分数线图',subtitle='2009-2019年'))
    c.render(diquname +'历年高考录取分数线图.html')
    print(diquname + '历年高考录取分数线图绘制完成。')


if __name__ == '__main__':
    start = time.time()
    diquname = '浙江'
    # diquname = input('请输入查询的省份:')
    yanz(diquname)
    print('爬虫已完毕，程序结束。')
    print("用时: {}".format(time.time() - start))
