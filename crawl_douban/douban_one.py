#coding=utf-8
import urllib.request
from bs4 import BeautifulSoup
import re
import json

def writeToFile(data):
    path='e:/test/douban.txt'
    with open(path,'w') as file:
        file.write(data)
        file.close()
    print('写入成功')

def searchByName(name):
    headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')
    opener = urllib.request.build_opener()
    opener.addheaders=[headers]
    #name = '季春奶奶'
    b = name.encode('utf-8')
    name_url = str(b).replace(r'\x','%').swapcase()[1:]
    #print(str(b).replace(r'\x','%').swapcase()[1:])
    url = 'https://movie.douban.com/subject_search?search_text='+name_url+'&cat=1002'
    #print(url)
    response = opener.open(url)
    page_data = response.read().decode('utf-8')
    #print(page_data)
    soup = BeautifulSoup(page_data,'html.parser')
    trs = soup.find('div',id="content").find_all('tr',attrs={"class":"item"})
    for tr in trs:
        print('详情链接：  '+tr.a['href'])
        writeToFile(tr.a['href'])
        #print('名字：  '+tr.a['title'])
        writeToFile(tr.a['title'])
        p = tr.find('div',attrs={"class":"pl2"}).find_all('p',attrs={"class":"pl"})[0].string
        print('时间/国家/演员：   '+p)
        writeToFile(p)
headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')
opener = urllib.request.build_opener()
opener.addheaders=[headers]
i=0
for i in range(1,2):
    page_start=i*20
    data = opener.open('https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start='+str(page_start)).read().decode('utf-8')
    json_data = json.loads(data)
    for one in json_data["subjects"]:
        print('名字：  '+one["title"])
        writeToFile(one["title"])
        print('评分：  '+one["rate"])
        writeToFile(one["rate"])
        print('图片：  '+one["cover"])
        writeToFile(one["cover"])
        searchByName(one["title"])
        print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-OVER*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
    

