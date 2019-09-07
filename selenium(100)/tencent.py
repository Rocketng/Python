import requests
import os
import json
import re
import sys
import urllib.request
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pymysql

def getQQurl():#获取腾讯新闻首页的所有新闻链接
   qqf = open("D:/news/腾讯新闻/plate.txt", "r")
   urls = qqf.readlines()  # 读取文件得到一个板块列表
   qqf.close()

   dt = time.localtime()
   ft = "%Y%m%d"
   nt = time.strftime(ft, dt)
   fo = open("D:/news/腾讯新闻/url/" + nt + ".txt", "w+")  # 创建txt保存所有链接

   UrlSet = set()   #用来过滤重复的新闻链接

   for url in urls:
       driver = webdriver.Firefox()
       driver.get(url)
       time.sleep(5)

       lst = driver.find_elements_by_class_name("list")
       datas = []  # 用来存放当前页面的新闻链接
       for ls in lst:
           time.sleep(5)
           datas = datas + ls.find_elements_by_tag_name('a')

       for data in datas:
           if data.text != "":
               link = data.get_attribute('href')
               if link not in UrlSet:
                   UrlSet.add(link)
                   fo.writelines(link+"\n")
       driver.close()

   fo.close()


def getQQtext():      #根据获取的链接依次爬取新闻正文并保存到本地和数据库中
    dt = time.localtime()
    ft = "%Y%m%d"
    nt = time.strftime(ft, dt)
    qqf = open("D:/news/腾讯新闻/url/"+nt+".txt","r")
    qqurl=qqf.readlines()  #读取文件得到一个链接列表
    i=0


    db = pymysql.connect('localhost', 'root', 'PFY132465', 'mydb', charset='utf8')  # 连接数据库
    cur = db.cursor()  # 创建游标
    sqlc = '''
        create table news(
        id int(11) not null auto_increment primary key,
        article text not null,
        dt varchar(20) not null,
        tittle varchar(50) not null
        )
        '''
    cur.execute(sqlc)  # 创建数据表

    # 遍历列表，请求网页，筛选出正文信息
    for qurl in qqurl:
        print(qurl)
        try:
            response = requests.get(qurl.strip())
            soup = BeautifulSoup(response.text, "lxml")
            title = soup.select('title')
            moment = soup.select('head > meta:nth-child(4)')         #发布时刻
            author = soup.select('a.author > div')
            content = soup.select('p')

            if(len(title)!=0) and (len(content)!=0):
                #将新闻写入文件
                fo = open("D:/news/腾讯新闻/url/" + nt + "use.txt", "a")
                fo_1 = open("D:/news/腾讯新闻/标题/" + nt +"_"+ str(i) + ".txt", "w+")
                fo_2 = open("D:/news/腾讯新闻/文章/" + nt +"_"+ str(i) + ".txt", "w+")
                print(title[0].text)
                fo.writelines(qurl)
                fo_1.writelines("    "+title[0].text+"\n")
                fo_1.writelines("    "+moment[0].get('content')+"\n")
                #fo_1.writelines("    "+author[0].text+"\n")
                article = ""
                for m in range(0,len(content)):
                    con = content[m].text
                    if(len(con) != 0):
                        fo_2.writelines("\n"+con)
                        article = article + "\n" + con
                    m += 1
                i += 1
                fo_1.close()
                fo_2.close()
                #将新闻写入数据库
                sqli = '''insert into news(article, dt, tittle)
                values('%s','%s','%s')
                ''' % (article, moment[0].get('content'), title[0].text)
                try:
                    cur.execute(sqli)  # 执行sql语句 ，插入数据
                    db.commit()  # 提交到数据库执行
                    print('导入数据库成功')
                except:
                    db.rollback()  # 如果发生错误则回滚
                    print('失败')


        except Exception as err:
            print(err)
    cur.close()

def main():
    getQQurl()
    getQQtext()

main()
