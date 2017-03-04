# coding=utf-8
import urllib.request
import json,re

def downLoadPic(image,title):
    try:
        image_data = urllib.request.urlopen(image).read()
        #.sleep(15)
        #image_path = 'e:/test/'+str(time.time())[:-4]+'.jpg'
        image_path = 'e:/test/English/'+title+'.jpg'
        print(image_path)
        with open(image_path,'wb') as image_file:
            image_file.write(image_data)
        image_file.close()
    except error.URLError as e:
        print(e.reason)
        print('download failed')

headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')
opener = urllib.request.build_opener()
opener.addheaders=[headers]
date = '2016-10-02'
json_url ='http://sentence.iciba.com/index.php?callback=jQuery183046760655497200787_1475315114224&c=dailysentence&m=getdetail&title='+date
response_data = opener.open(json_url).read().decode('utf-8')
delete = 'jQuery183046760655497200787_1475315114224'
jdata = str(response_data).replace(delete,'')[1:-1]
#print(jdata)
#pattern_ = re.compile(r'.+(.*)+$')
#print(pattern_.findall(response_data)[0])
json_data = json.loads(jdata)
print(json_data["content"])
print(json_data["note"])
print(json_data["tts"])
print(json_data["tts_size"])
print(json_data["picture2"])
pattern = re.compile(r'http://cdn.iciba.com/news/word/big_(.*?)b.jpg')
title_1 = pattern.findall(json_data["picture2"]) #返回的是元组 所以要加[]
downLoadPic(json_data["picture2"],title_1[0])
#下载音频
urllib.request.urlretrieve(json_data["tts"],'e:/test/English/'+title_1[0]+'.mp3')
