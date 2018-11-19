# -*- coding:utf-8 -*-
import datetime
import re
import time

import pymysql

from lxml import etree
from selenium import webdriver

driver = webdriver.Chrome()


def get_first_page(url):

    driver.get(url)
    html = driver.page_source
    return html



# 可以尝试第二种解析方式，更加容易做计算
def parse_stock_note(html):

    selector = etree.HTML(html)
    code = selector.xpath('//*[@id="pro_body"]/center/div[5]/h1/strong/text()')
    profits= selector.xpath('//*[@id="right_col"]/table/tbody/tr[1]/td/table/tbody/tr[7]/td/text()')
    d_2018= "".join(profits[1][:-3].split(","))
    d_2017= "".join(profits[2][:-3].split(","))
    d_2016= "".join(profits[3][:-3].split(","))

    big_tuple = (code[0],d_2018,d_2017,d_2016)
    return big_tuple






def insertDB(content):
    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JS',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    try:
        cursor.executemany('insert into js_FinData (coding,industry,d2018,d2017,d2016) values (%s,%s,%s,%s,%s)', content)
        connection.commit()
        connection.close()
        print('向MySQL中添加数据成功！')
    except TypeError :
        pass

#
if __name__ == '__main__':

    connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', db='JS',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cur = connection.cursor()
    #sql 语句
    for num in range(1,3600):
        big_list = []
        sql = 'select coding from js_infos where id = %s ' % num
        # #执行sql语句
        cur.execute(sql)
        # #获取所有记录列表
        data = cur.fetchone()
        num_coding = data['coding']
        url = 'https://profile.yahoo.co.jp/consolidate/' + str(num_coding)


        html = get_first_page(url)
        content = parse_stock_note(html)
        for item in content:
            big_list.append(item)
        # 加入查询板块的操作
        sql = 'select * from js_infos_finanData where id = %s ' % num
        # #执行sql语句
        cur.execute(sql)
        # #获取所有记录列表
        data = cur.fetchone()
        data_industry = data['industry']
        big_list.append(data_industry)
        big_list_tuple = tuple(big_list)
        finanl_content = []
        finanl_content.append(big_list_tuple)  # 是要带着元括号操作，
        insertDB(finanl_content)
        print(datetime.datetime.now())



#
# create table js_FinData(
# id int not null primary key auto_increment,
# coding varchar(50),
# industry varchar(8),
# d2018 varchar(20),
# d2017 varchar(20),
# d2016 varchar(20)
# ) engine=InnoDB  charset=utf8;