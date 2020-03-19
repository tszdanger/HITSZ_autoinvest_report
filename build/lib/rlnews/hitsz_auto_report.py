# 本脚本用来自动生成投资报告
# this script is used to gene the invest report automatically

'''
智能证券投资报告：题目格式为：2020投资记录/策略/心得等
（一周最少一次，在周日之前完成，首次在海知社区发帖`提交，后续以跟帖形式提交，最后可以汇总为投资记录，供最后总结参考）
报告格式示例：
1.	现状分析：（多选：上证指数、深成指、创业板、个体品种例如茅台、群体版块例如5G,等等）在（最近一（周、月、年）、今年、本月、周以来），涨幅XX%，收盘XX，
走势呈（稳步、波动）（上、下）行，主要因素影响：国际形势、国内经济形势、政策面、资金面、技术面，……等个人看法。
2.	未来预期：基于什么理由，看好XX，看淡什么？
3.	操作策略：采取（进取（股票等波动大的）、稳健（债券等波动小的、保守（现金等价物或者空仓）），混合）策略，仓位比例配置（股票、债券、现金），……
4.	提高效率：（尽可能借助自动化工具）：例如：多因子选（股、债），数据分析，……
5.	问题和建议

围绕三个重点：理性投资、个性化，提高效率

'''

#  我个人偏向于投资几个固定股票


# import requests
# from bs4 import BeautifulSoup
import re
import random
import time
# from fake_useragent import UserAgent
# from collections import OrderedDict
# import smtplib
# from email.mime.text import MIMEText

import time

import easyquotation

# 股票仓
GPC = ['600518','000623','002118','000423','000999','600222','600129','600479','600000','601818','601288','601166','000001']

GPC_STRATAGE =[random.randint(0,4) for i in range(len(GPC))]



# 现状分析,这里调用sina/tencent接口
a = time.strftime("%Y-%m-%d ", time.localtime())


quotation = easyquotation.use('sina')

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
            ratio = ratio_self
            result.append('买入')
        elif GPC_STRA[i] < strategy-0.3:
            result.append('卖出')
        else:
            result.append('不变')
    return result


if __name__ == '__main__':
    strategy = 0  # 0表示保守，1表示稳健，2表示激进
    NLP_analysis = 0  # 0-1数值根据市场反应自适应
    prediction = 0  # 0-1 数值表示对未来市场的期待
    ratio_self = 0.6  # 个人设计股票占比



    #
    # res = requests.get('https://news.sina.com.cn/roll/#pageid=153&lid=2518&k=&num=50&page=1')  # 获取目标网页
    # res.encoding = 'utf-8'  # 抓取网页出现乱码
    # print(res.text)
    # soup = BeautifulSoup(res.text, 'html.parser')  # 爬取网页
    #
    #
    # print(soup.prettify())
    # print('1')


filename = 'report' + str(a) + '.txt'
with open(filename, 'w') as f:
    kaitou = '每日报告基于每日的上证指数综合生成。同时给出总体的政策面、经济面等导向信息以及个人选择的理由。\n \
进而针对股票仓中的每只股票单独进行分析，给出其操作意见和操作的原因\n'
    f.write(kaitou)
    content1 = GZXXXX()
    for i in content1:
        f.write(i)
    content1 = GPXXXX(GPC)
    for i in content1:
        f.write(i)




    # for i in GPC:
    #     print(quotation.real(i))
