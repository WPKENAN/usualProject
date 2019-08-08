# -*- coding: utf-8 -*-
"""
Created on Tue May  7 13:39:20 2019

@author: mac
"""


import csv
#import codes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import requests
from bs4 import BeautifulSoup
# import pyecharts
import re
import cv2 as cv

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication




all_GDP = []
per_GDP = []
GDP_Growth = []
CPI_Growth = []
Saving = []
Population = []
all_GDP_Compare = []
per_GDP_Compare = []
GDP_Growth_Compare = []
Population_Compare = []

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return





def fill_List(soup, lst):
    df = pd.DataFrame(columns = lst)
    data = soup.find_all('tr')
    for tr in data:
        ltd = tr.find_all('td')
        if len(ltd)!=len(lst):
            continue
        ss = pd.Series([td.string for td in ltd], index = df.columns)
        df = df.append(ss, ignore_index = True)
    return df

def draw_avg_max_min(value_country,title=""):
    print(value_country)
    value_country.sort(reverse=0);
    print(value_country)

    value=[]
    name_list=[]
    for i in range(len(value_country)):
        if value_country[i][1] in ['欧盟地区','全世界']:
            continue
        value.append(value_country[i][0])
        name_list.append(value_country[i][1])

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig = plt.figure()
    # 画柱子
    ax1 = fig.add_subplot(111)
    ax1.barh(list(range(len(value)))[:100],value[-100:],tick_label=name_list[-100:])
    # 画折线图
    ax2 = ax1.twinx()  # 这个很重要噢
    ax2.plot([np.mean(value),np.mean(value)],[0,len(value[-100:])],c='r',label='Mean')
    ax2.plot([np.max(value),np.max(value)],[0,len(value[-100:])], c='g',label='Max')
    ax2.plot([np.min(value), np.min(value)],[0, len(value[-100:])],  c='b',label='Min')

    plt.xlabel('Dollar')
    plt.title(title)
    plt.legend()
    # plt.show()
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(10.5, 18.5)
    fig.savefig(title+'.png', dpi=96)
    plt.close()

def plotTime(years,countries,title,x,y):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    print(years)
    for key in countrise:
        plt.plot(years,countrise[key],label=key)
    plt.legend()
    plt.ylabel(y)
    plt.xlabel(x)
    plt.title(title)
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(10.5, 18.5)
    fig.savefig(title + '.png', dpi=96)
    plt.close()
    # plt.show()


if __name__=="__main__":

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    url_1 = 'https://www.kuaiyilicai.com/stats/global/yearly_overview/g_gdp.html'
    url_2 = 'https://www.kuaiyilicai.com/stats/global/yearly_overview/g_gdp_per_capita.html'
    url_3 = 'https://www.kuaiyilicai.com/stats/global/yearly_overview/g_gdp_growth.html'
    url_4 = 'https://www.kuaiyilicai.com/stats/global/yearly_overview/g_inflation_consumer_prices.html'
    url_5 = 'https://www.kuaiyilicai.com/stats/global/yearly_overview/g_gross_saving_current_usd.html'
    url_6 = 'https://www.kuaiyilicai.com/stats/global/yearly_overview/g_population_total.html'
    url_7 = 'https://www.kuaiyilicai.com/stats/global/yearly_per_country/g_gdp/chn-jpn-ind-usa-deu.html' #GDP对比
    url_8 = 'https://www.kuaiyilicai.com/stats/global/yearly_per_country/g_gdp_per_capita/chn-jpn-ind-usa-deu.html'  #人均GDP
    url_9 = 'https://www.kuaiyilicai.com/stats/global/yearly_per_country/g_gdp_growth/chn-jpn-ind-usa-deu.html' #GDP增速
    url_10 = 'https://www.kuaiyilicai.com/stats/global/yearly_per_country/g_population_total/chn-jpn-ind-usa-deu.html'  #人口增速


    lst1 = ['排名', '国家\地区', '所在洲', '年份', 'GDP（美元计）']
    lst2 = ['年份', '中国', '日本', '印度', '美国','德国']
    html_1 = getHTMLText(url_1)
    html_2 = getHTMLText(url_2)
    html_3 = getHTMLText(url_3)
    html_4 = getHTMLText(url_4)
    html_5 = getHTMLText(url_5)
    html_6 = getHTMLText(url_6)
    html_7 = getHTMLText(url_7)
    html_8 = getHTMLText(url_8)
    html_9 = getHTMLText(url_9)
    html_10 = getHTMLText(url_10)
    soup_1 = BeautifulSoup(html_1, "html.parser")
    soup_2 = BeautifulSoup(html_2, "html.parser")
    soup_3 = BeautifulSoup(html_3, "html.parser")
    soup_4 = BeautifulSoup(html_4, "html.parser")
    soup_5 = BeautifulSoup(html_5, "html.parser")
    soup_6 = BeautifulSoup(html_6, "html.parser")
    soup_7 = BeautifulSoup(html_7, "html.parser")
    soup_8 = BeautifulSoup(html_8, "html.parser")
    soup_9 = BeautifulSoup(html_9, "html.parser")
    soup_10 = BeautifulSoup(html_10, "html.parser")
    all_GDP = fill_List(soup_1, lst1)
    per_GDP = fill_List(soup_2,lst1)
    GDP_Growth = fill_List(soup_3,lst1)
    CPI_Growth = fill_List(soup_4,lst1)
    Saving = fill_List(soup_5,lst1)
    Population = fill_List(soup_6, lst1)
    all_GDP_Compare = fill_List(soup_7,lst2)
    per_GDP_Compare = fill_List(soup_8,lst2)
    GDP_Growth_Compare = fill_List(soup_9,lst2)
    Population_Compare = fill_List(soup_10, lst2)

    #
    #p1
    print(all_GDP)
    print(all_GDP['GDP（美元计）'].values[0])
    value_country=[]
    for i in range(len(all_GDP)):
        value_country.append([eval(re.findall('\((.+?)\)',all_GDP['GDP（美元计）'].values[i])[0].replace(',','')),all_GDP['国家\地区'].values[i]])
    draw_avg_max_min(value_country,"全球各国的GDP TOP-100")

    #p2
    value_country=[]
    for i in range(len(per_GDP)):
        value=re.findall('\((.+?)\)',per_GDP['GDP（美元计）'].values[i])
        if len(value)==0:
            value_country.append([eval(per_GDP['GDP（美元计）'].values[i]),per_GDP['国家\地区'].values[i]])
        else:
            value_country.append([eval(value[0].replace(',','')),per_GDP['国家\地区'].values[i]])
    # print(value_country)
    draw_avg_max_min(value_country,"全球各国人均GDP TOP-100")

    # p3
    print(GDP_Growth)
    # print(per_GDP['GDP（美元计）'].values[77])
    value_country = []
    for i in range(len(GDP_Growth)):
        value = GDP_Growth['GDP（美元计）'].values[i]
        value_country.append([eval(value.replace('%', '')), GDP_Growth['国家\地区'].values[i]])
    # print(value_country)
    draw_avg_max_min(value_country, "各国GDP增长率 TOP-100")

    # #p4
    print(CPI_Growth)
    # print(per_GDP['GDP（美元计）'].values[77])
    value_country = []
    for i in range(len(CPI_Growth)):
        value = CPI_Growth['GDP（美元计）'].values[i]
        value_country.append([eval(value.replace('%', '')), CPI_Growth['国家\地区'].values[i]])
    # print(value_country)
    draw_avg_max_min(value_country, "各国通货膨胀率增长率 TOP-100")

    # p5
    value_country=[]
    for i in range(len(Saving)):
        value=re.findall('\((.+?)\)',Saving['GDP（美元计）'].values[i])
        if len(value)==0:
            value_country.append([eval(Saving['GDP（美元计）'].values[i]),Saving['国家\地区'].values[i]])
        else:
            value_country.append([eval(value[0].replace(',','')),Saving['国家\地区'].values[i]])
    # print(value_country)
    draw_avg_max_min(value_country,"各国货币储备 TOP-100")

    #p6
    value_country=[]
    # print(Population)
    for i in range(len(Population)):
        value=re.findall('\((.+?)\)',Population['GDP（美元计）'].values[i])
        if len(value)==0:
            value_country.append([eval(Population['GDP（美元计）'].values[i]),Population['国家\地区'].values[i]])
        else:
            value_country.append([eval(value[0].replace(',','')),Population['国家\地区'].values[i]])
    # print(value_country)
    draw_avg_max_min(value_country,"各国人口 TOP-100")

    # p7
    countrise={}
    for country in all_GDP_Compare.keys().values:
        if country=='年份':
            continue
        countrise[country]=[];
        for i in range(len(all_GDP_Compare)):
            value = re.findall('\((.+?)\)', all_GDP_Compare[country].values[i])
            if len(value)==0:
                # print(int(all_GDP_Compare[country].values[i]))
                if len(all_GDP_Compare[country].values[i])==1:
                    countrise[country].append(0)
                else:
                    countrise[country].append(eval(all_GDP_Compare[country].values[i]))
            else:
                countrise[country].append(eval(value[0].replace(',','')))
    years=[]
    for i in range(len(all_GDP_Compare)):
        years.append(eval(all_GDP_Compare['年份'].values[i].strip('年')))
    plotTime(years,countrise,'总体GDP比较','年份','美元')

    # p8
    countrise={}
    for country in per_GDP_Compare.keys().values:
        if country=='年份':
            continue
        countrise[country]=[];
        for i in range(len(per_GDP_Compare)):
            value = re.findall('\((.+?)\)', per_GDP_Compare[country].values[i])
            if len(value)==0:
                # print(int(all_GDP_Compare[country].values[i]))
                if len(per_GDP_Compare[country].values[i])==1:
                    countrise[country].append(0)
                else:
                    countrise[country].append(eval(per_GDP_Compare[country].values[i]))
            else:
                countrise[country].append(eval(value[0].replace(',','')))
    years=[]
    for i in range(len(per_GDP_Compare)):
        years.append(eval(per_GDP_Compare['年份'].values[i].strip('年')))
    plotTime(years,countrise,'人均GDP比较','年份','美元')



    #p9
    countrise = {}
    for country in GDP_Growth_Compare.keys().values:
        if country == '年份':
            continue
        countrise[country] = [];
        for i in range(len(GDP_Growth_Compare)):
            value = re.findall('\((.+?)\)', GDP_Growth_Compare[country].values[i])
            if len(value) == 0:
                # print(int(all_GDP_Compare[country].values[i]))
                if len(GDP_Growth_Compare[country].values[i]) == 1:
                    countrise[country].append(0)
                else:
                    countrise[country].append(eval(GDP_Growth_Compare[country].values[i].strip('%')))
            else:
                countrise[country].append(eval(value[0].replace('%', '')))
    years = []
    for i in range(len(GDP_Growth_Compare)):
        years.append(eval(GDP_Growth_Compare['年份'].values[i].strip('年')))
    plotTime(years, countrise, 'GDP增速比较','年份','%')

    # p10
    countrise={}
    for country in Population_Compare.keys().values:
        if country=='年份':
            continue
        countrise[country]=[];
        for i in range(len(Population_Compare)):
            value = re.findall('\((.+?)\)', Population_Compare[country].values[i])
            if len(value)==0:
                # print(int(all_GDP_Compare[country].values[i]))
                if len(Population_Compare[country].values[i])==1:
                    countrise[country].append(0)
                else:
                    countrise[country].append(eval(Population_Compare[country].values[i]))
            else:
                countrise[country].append(eval(value[0].replace(',','')))


    years=[]
    for i in range(len(Population_Compare)):
        years.append(eval(Population_Compare['年份'].values[i].strip('年')))
    plotTime(years,countrise,'人口比较','年份','人数')


    #回归
    population = {}
    for country in Population_Compare.keys().values:
        if country == '年份':
            continue
        population[country] = [];
        for i in range(len(Population_Compare)):
            value = re.findall('\((.+?)\)', Population_Compare[country].values[i])
            if len(value) == 0:
                # print(int(all_GDP_Compare[country].values[i]))
                if len(Population_Compare[country].values[i]) == 1:
                    population[country].append(0)
                else:
                    population[country].append(eval(Population_Compare[country].values[i]))
            else:
                population[country].append(eval(value[0].replace(',', '')))

    gdp = {}
    for country in all_GDP_Compare.keys().values:
        if country == '年份':
            continue
        gdp[country] = [];
        for i in range(len(all_GDP_Compare)):
            value = re.findall('\((.+?)\)', all_GDP_Compare[country].values[i])
            if len(value) == 0:
                # print(int(all_GDP_Compare[country].values[i]))
                if len(all_GDP_Compare[country].values[i]) == 1:
                    gdp[country].append(0)
                else:
                    gdp[country].append(eval(all_GDP_Compare[country].values[i]))
            else:
                gdp[country].append(eval(value[0].replace(',', '')))

    #回归印度population 1959-2017 gdp 1960-2017
    x=np.array(population['印度'])
    x=x.reshape(len(x),1)
    x=np.hstack((x,np.zeros((len(x),1))+1))
    print(x)
    y=np.array(gdp['印度'])
    y=y.reshape(len(y),1)
    x=x[0:len(y),:]
    print(x.shape)
    print(y.shape)
    a=np.linalg.lstsq(x, y)[0]
    plt.scatter(x[:,0],y)
    print([min(x[:,0]),max(x[:,0])])
    print(a[0,0],a[1,0])
    # print([min(x[:,0]),max(x[:,0])]*a[0,0]+a[1,0])
    plt.plot([min(x[:,0]),max(x[:,0])],np.array([min(x[:,0]),max(x[:,0])])*a[0,0]+a[1,0])
    # plt.show()
    plt.title("印度 GDP-人口 一元回归")
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(10.5, 18.5)
    fig.savefig("印度 GDP-人口 一元回归" + '.png', dpi=96)
    plt.close()

    # 回归印度population 1959-2017 gdp 1960-2017
    x = np.array(population['中国'])
    x = x.reshape(len(x), 1)
    x = np.hstack((x, np.zeros((len(x), 1)) + 1))
    print(x)
    y = np.array(gdp['中国'])
    y = y.reshape(len(y), 1)
    x = x[0:len(y), :]
    print(x.shape)
    print(y.shape)
    a = np.linalg.lstsq(x, y)[0]
    plt.scatter(x[:, 0], y)
    print([min(x[:, 0]), max(x[:, 0])])
    print(a[0, 0], a[1, 0])
    # print([min(x[:,0]),max(x[:,0])]*a[0,0]+a[1,0])
    plt.plot([min(x[:, 0]), max(x[:, 0])], np.array([min(x[:, 0]), max(x[:, 0])]) * a[0, 0] + a[1, 0])
    # plt.show()
    plt.title("中国 GDP-人口 一元回归")
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(10.5, 18.5)
    fig.savefig("中国 GDP-人口 一元回归" + '.png', dpi=96)
    plt.close()



