import csv
import json
import re
import os
import sys
import time

import requests
from pymysql import *
from selenium.webdriver.chrome.service import Service

from utils.query import querys


# 房名 封面 市区 地区 详情地址 房型详情 建面 是否具有预售证 每平价格 房屋的装修情况（毛坯，简装修） 公司 房屋类型（别墅） 交房时间 开盘时间 标签 总价区间 售房情况（在售）  详情链接

def init():
    if not os.path.exists('hourseInfoData.csv'):
        with open('hourseInfoData.csv', 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'title',
                'cover',
                'city',
                'region',
                'address',
                'rooms_desc',
                'area_range',
                'all_ready',
                'price',
                'hourseDecoration',
                'company',
                'hourseType',
                'on_time',
                'open_date',
                'tags',
                'totalPrice_range',
                'sale_status',
                'detail_url'
            ])


def writerRow(row):
    with open('hourseInfoData.csv', 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)


def get_data(url):
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    #     'cookie':'ab_jid=d9487f4b7f10455d0e19e99c9bfac465c8f0; ab_jid_BFESS=d9487f4b7f10455d0e19e99c9bfac465c8f0; BAIDUID_BFESS=A4DFD111A6D28D96FD351F5F8698D5A8:FG=1; BDUSS_BFESS=x1Y2JHekU2VlhSbE9DSUJ3MEw0VGdrLVU2SnVYR2ZhfjZaZHVsNXZGa2ZKQVpuRVFBQUFBJCQAAAAAAAAAAAEAAABvNvVAsKLLubbZyPa1qTU1OQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB-X3mYfl95mY0; H_WISE_SIDS_BFESS=60272_60515_60599_60628_60663_60677_60696_60727; ZFY=mGmzvY0kxhohK5QVXflEqpfOl7gvg3fXlkwpPVrZqLo:C; ab_bid=f8abab09d374d800d9487f4b7f10455d0e18; ab_sr=1.0.1_YjZhZDM3NjZhNTVhZDQ3YTcwOGRhZTEzYzcwNmM2NDUxOGVjNjI4YzQ3MmVlM2ZkNGM4Y2Q4ZTBhMGFiZDVlMTNmOGZjZGQ1YzMxMTIxZThjYzM1ZmMxOTFkNTA5ZTY5OWRmNTViMTU4YTQyM2U1YjU4NmM3NzkwNjRmY2VjMmU0MmVjNzdkM2JhOTUxZDk5MDk1NTEzNGYzMWIyODYyODBkZDZlYTI4ZmMzNjdmMzZhZDU2OGY1NDU2MjljOGY0NzIxNjJlNDhiNTk5N2VjM2IyYWFhMmJjM2UwM2IyNGI=',
    #     'Referer':'https://bd.fang.lianjia.com/loupan/pg2/'
    # }
    # response = requests.get(url,headers)
    # if response.status_code == 200:
    #     return response.json()['data']['list']
    # else:
    #     return None
    # print(url)
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    service = Service('./chromedriver.exe')
    options = webdriver.ChromeOptions()
    # options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_experimental_option('debuggerAddress', 'localhost:9222')  # 指定远程调试端口
    # options.add_argument('--headless')  # 确保浏览器始终以无头模式运行
    browser = webdriver.Chrome(service=service, options=options)

    try:
        browser.get(url)
        # 获取页面的JSON数据
        data = json.loads(browser.find_element("tag name", "body").text)
        return data['data']['list']  # 返回需要的数据部分
    except:
        pass


def parse_data(hourseDataList, city, url):
    for hourseInfo in hourseDataList:
        title = hourseInfo['title']
        cover = hourseInfo['cover_pic']
        region = hourseInfo['district']
        address = hourseInfo['address']
        rooms_desc = json.dumps(hourseInfo['frame_rooms_desc'].replace('居', '').split('/'))
        area_range = json.dumps(hourseInfo['resblock_frame_area_range'].replace('㎡', '').split('-'))
        all_ready = hourseInfo['permit_all_ready']
        price = hourseInfo['average_price']
        hourseDecoration = hourseInfo['decoration']
        company = hourseInfo['developer_company'][0]
        hourseType = hourseInfo['house_type']
        on_time = hourseInfo['on_time']
        open_date = hourseInfo['open_date']
        tags = json.dumps(hourseInfo['tags'])
        totalPrice_range = json.dumps(hourseInfo['reference_total_price'].split('-'))
        sale_status = hourseInfo['process_status']
        detail_url = 'https://' + re.search('//(.*)/loupan/pg\d/\?_t=1', url).group(1) + hourseInfo['url']
        writerRow([
            title,
            cover,
            city,
            region,
            address,
            rooms_desc,
            area_range,
            all_ready,
            price,
            hourseDecoration,
            company,
            hourseType,
            on_time,
            open_date,
            tags,
            totalPrice_range,
            sale_status,
            detail_url
        ])


def save_to_sql():
    with open('hourseInfoData.csv', 'r', encoding='utf-8') as reader:
        readerCsv = csv.reader(reader)
        next(readerCsv)
        for h in readerCsv:
            querys('''
                insert into hourse_info(title,cover,city,region,address,rooms_desc,area_range,all_ready,price,hourseDecoration,company,hourseType,on_time,open_date,tags,totalPrice_range,sale_status,detail_url)
                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''', [
                h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10], h[11], h[12], h[13], h[14], h[15],
                h[16], h[17]
            ])


def main():
    init()
    with open('./cityData.csv', 'r', encoding='utf-8') as readerFile:
        reader = csv.reader(readerFile)
        next(reader)
        for city in reader:
            try:
                for page in range(1, 20):
                    url = 'https:' + re.sub('pg1', 'pg' + str(page), city[1])
                    print('正在爬取 %s 城市的房屋数据正在第 %s 页 路径为：%s' % (
                        city[0],
                        page,
                        url
                    ))
                    hourseDetailList = get_data(url)
                    parse_data(hourseDetailList, city[0], url)
            except:
                pass


if __name__ == '__main__':
    main()

    # save_to_sql()
