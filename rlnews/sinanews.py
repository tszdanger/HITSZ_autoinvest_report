# -*- coding: utf-8 -*-

"""
新浪新闻数据接口
"""
import random
import time
import easyquotation
import re
import json
import random
import lxml.html
import lxml.etree
import pandas as pd
from datetime import datetime

from rlnews import sina_constants as cts
from rlnews.utils.downloader import Downloader
from rlnews.utils.disk_cache import DiskCache

no_cache_downloader = Downloader(cache=None)
disk_cache_downloader = Downloader(cache=DiskCache())


#走势呈（稳步、波动）（上、下）行，
def zoushi(GP):
    isdown = 0  # 0表示涨了
    isbodong = 0 # 0 表示稳定
    zhangfu = round(((GP['now'] - GP['open'])),3)
    zfbfb = round(((GP['now'] - GP['open']) / GP['open']),3)
    isdown = 0 if zhangfu>0 else 1
    if(abs(GP['high'] - GP['low']) >(10*abs(zhangfu))):
        isbodong = 1
    zoushi = '稳定' if isbodong==0 else '波动'
    updown = '上行' if isdown==0 else '下行'
    total_info = '这只股票今日走势总体而言'+zoushi+updown+'\n'
    add = '建议买入\n' if random.randint(0,1)==1 else '建议卖出\n'
    total_info += add
    return total_info

#主要因素影响：国际形势、国内经济形势、政策面、资金面、技术面，……等个人看法。

# 输出股票详细信息和波动信息
def GPXXXX(GP_LIST):
    total_detail=[]
    for GP_NUM in GP_LIST:
        GP = quotation.real(GP_NUM)[GP_NUM]
        zhangfu = round(((GP['now']-GP['open'])),3)
        zfbfb  =round(((GP['now']-GP['open'])/GP['open']),3)
        each_GP = '今日' + GP['name'] + '开盘为：' + str(GP['open']) +'\n' \
        '收盘为:' + str(GP['now']) +'\n' \
        '涨幅为' + str(zhangfu) + '涨幅百分比' + str(zfbfb)+'\n'
        total_detail.append(each_GP)
        total_detail.append(zoushi(GP))
    return total_detail



def GZXXXX():
    total_detail = []
    market = quotation.stocks(['sh000001', 'sz000001'], prefix=True)
    # 名称
    name = market['sh000001']['name']
    # 涨幅
    zhangfu = round((market['sh000001']['now'] - market['sh000001']['open']),3)
    # 涨幅百分比
    zfbfb = round(((zhangfu / market['sh000001']['open'])),3)


    line0 = a +'大盘情况分析\n'
    line1 = '今日' + name + '开盘为：' + str(market['sh000001']['open']) +'\n' \
            '收盘为:' + str(market['sh000001']['now']) +'\n' \
            '涨幅为' + str(zhangfu) + '涨幅百分比' + str(zfbfb)+'\n'
    total_detail.append(line0)
    total_detail.append(line1)
    return total_detail

def get_strategy(GPC_STRA,NLP_analysis,strategy):
    result = []
    NLP_analysis = random.random()
    for i in range(len(GPC_STRA)):
        GPC_STRA[i] = GPC_STRA[i]*(0.5+NLP_analysis)

        if GPC_STRA[i] > strategy:
            # ratio = ratio_self
            result.append('买入')
        elif GPC_STRA[i] < strategy-0.3:
            result.append('卖出')
        else:
            result.append('不变')
    return result


def get_rolling_news_csv(top=50, get_content=True, classify=None, path=None):
    """
    获取新浪滚动新闻并保存成csv文件
    :param top: int, 获取的滚动新闻条数，默认为50
    :param get_content: bool, 是否获取新闻内容，默认为True
    :param classify: str, 获取的滚动新闻的类别，默认为None，即"2509:全部"
    :param path: str, 文件保存路径
    """
    df = get_rolling_news(top=top, get_content=get_content, classify=classify)
    if not path:
        path = 'news.csv'
    df.to_csv(path, index=False, encoding='utf-8')
    return df['title']

def get_rolling_news(top=50, get_content=True, classify=None):
    """
    获取新浪滚动新闻
    :param top: int, 获取的滚动新闻条数，默认为50
    :param get_content: bool, 是否获取新闻内容，默认为True
    :param classify: str, 获取的滚动新闻的类别，默认为None，即"2509:全部"
    :return: pd.DataFrame, 新闻信息数据框
    """
    if classify:
        assert classify in cts.classifications, (
            '请设置 classify 为 {}中的一个'.format(cts.classifications)
        )

    lid = cts.classification2lid.get(classify, '2509')
    classify = cts.lid2classification[lid]
    num_list = [cts.max_num_per_page] * (top // cts.max_num_per_page)
    last_page_num = top % cts.max_num_per_page
    if last_page_num:
        num_list += [last_page_num]

    df_data = []
    for page, num in enumerate(num_list, start=1):
        r = random.random()
        url = cts.template_url.format(lid, num, page, r)
        response = no_cache_downloader(url)
        response_dict = json.loads(response)
        data_list = response_dict['result']['data']

        for data in data_list:
            ctime = datetime.fromtimestamp(int(data['ctime']))
            ctime = datetime.strftime(ctime, '%Y-%m-%d %H:%M')
            url = data['url']
            row = [classify, data['title'], ctime,
                   url, data['wapurl'], data['media_name'], data['keywords']]
            if get_content:
                row.append(get_news_content(url))
            df_data.append(row)
    df = pd.DataFrame(df_data, columns=cts.columns if get_content else cts.columns[:-1])
    return df


def get_rolling_news_url(top=50, classify=None):
    """
    获取新浪滚动新闻url
    :param top: int, 获取的滚动新闻条数，默认为50
    :param classify: str, 获取的滚动新闻的类别，默认为None，即"2509:全部"
    :return: pd.DataFrame, 新闻信息数据框
    """
    if classify:
        assert classify in cts.classifications, (
            '请设置 classify 为 {}中的一个'.format(cts.classifications)
        )

    lid = cts.classification2lid.get(classify, '2509')
    num_list = [cts.max_num_per_page] * (top // cts.max_num_per_page)
    last_page_num = top % cts.max_num_per_page
    if last_page_num:
        num_list += [last_page_num]

    urls = []
    for page, num in enumerate(num_list, start=1):
        r = random.random()
        url = cts.template_url.format(lid, num, page, r)
        response = no_cache_downloader(url)
        response_dict = json.loads(response)
        data_list = response_dict['result']['data']
        for data in data_list:
            url = data['url']
            urls.append(url)
    return urls


def get_news_content(url):
    """
    获取新闻内容
    :param url: str, 新闻链接
    :return: str, 新闻内容
    """
    content = ''
    try:
        text = disk_cache_downloader(url)
        html = lxml.etree.HTML(text)
        res = html.xpath('//*[@id="artibody" or @id="article"]//p')
        p_str_list = [lxml.etree.tostring(node).decode('utf-8') for node in res]
        p_str = ''.join(p_str_list)
        html_content = lxml.html.fromstring(p_str)
        content = html_content.text_content()
        # 清理未知字符和空白字符
        content = re.sub(r'\u3000', '', content)
        content = re.sub(r'[ \xa0?]+', ' ', content)
        content = re.sub(r'\s*\n\s*', '\n', content)
        content = re.sub(r'\s*(\s)', r'\1', content)
        content = content.strip()
    except Exception as e:
        print('get_news_content(%s) error:' % url, e)
    return content





if __name__ == '__main__':
    market_title = get_rolling_news_csv(top=5, get_content=True, classify='全部')

    strategy = 0  # 0表示保守，1表示稳健，2表示激进
    NLP_analysis = 0  # 0-1数值根据市场反应自适应
    prediction = 0  # 0-1 数值表示对未来市场的期待
    ratio_self = 0.6  # 个人设计股票占比
    # 股票仓
    GPC = ['600518', '000623', '002118', '000423', '000999', '600222', '600129', '600479', '600000', '601818', '601288',
           '601166', '000001']

    GPC_STRATAGE = [random.randint(0, 4) for i in range(len(GPC))]

    # 现状分析,这里调用sina/tencent接口
    a = time.strftime("%Y-%m-%d ", time.localtime())

    quotation = easyquotation.use('sina')

    filename = 'report' + str(a) + '.txt'
    with open(filename, 'w') as f:
        kaitou = '每日报告基于每日的上证指数综合生成。同时给出总体的政策面、经济面等导向信息以及个人选择的理由。\n \
    进而针对股票仓中的每只股票单独进行分析，给出其操作意见和操作的原因\n'
        f.write(kaitou)
        shichang = '当前金融市场重磅新闻有:\n'
        f.write(shichang)

        for i in market_title:
            i = i+'\n'
            f.write(i)
        content1 = GZXXXX()
        for i in content1:
            f.write(i)
        content1 = GPXXXX(GPC)
        for i in content1:
            f.write(i)

