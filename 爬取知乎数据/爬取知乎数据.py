#coding:utf-8
import requests
import http.cookiejar as cookielib
import re
import time
import os.path
import gzip

from PIL import Image
import pymysql
from bs4 import BeautifulSoup

db = pymysql.connect("localhost","root","123456","python",charset='utf8')

cursor = db.cursor()

# 构造 Request headers
#agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
headers = {
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def get_xsrf():
    '''_xsrf 是一个动态变化的参数'''
    index_url = 'http://www.zhihu.com'
    # 获取登录时需要用到的_xsrf
    index_page = session.get(index_url, headers=headers)
    html = index_page.text
    pattern = r'name="_xsrf" value="(.*?)"'
    # 这里的_xsrf 返回的是一个list
    _xsrf = re.findall(pattern, html)
    return _xsrf[0]

def ungzip(data):
    try: # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data

# 获取验证码
def get_captcha():
    t = str(int(time.time()*1000))
    captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url,allow_redirects=False).status_code
    if int(x=login_code) == 200:
        return True
    else:
        print('加载cookies失败或者没有登陆'+str(login_code))
        return False



def login(secret, account):
    # 通过输入的用户名判断是否是手机号
    if re.match(r"^1\d{10}$", account):
        print("手机号登录 \n")
        post_url = 'https://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': get_xsrf(),
            'password': secret,
            'remember_me': 'true',
            'phone_num': account,
        }
    else:
        print("邮箱登录 \n")
        post_url = 'https://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': get_xsrf(),
            'password': secret,
            'remember_me': 'true',
            'email': account,
        }
    try:
        # 不需要验证码直接登录成功
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = login_page.text
        print(login_code)
    except:
        # 需要输入验证码后才能登录成功
        postdata["captcha"] = get_captcha()
        login_page = session.post(post_url, data=postdata, headers=headers)
        login_code = eval(login_page.text)
        print(login_code['msg'])
    session.cookies.save()

try:
    input = raw_input
except:
    pass
name_list=[]
hasSavelist = []
#把表里的名字放进列表
def hasSaveName():
    sqlq = "select username from zhihu_personal;"
    try:
        cursor.execute(sqlq)
        results = cursor.fetchall()
        print(len(results))
        for row in results:
            hasSavelist.append(row[0])
        print(len(hasSavelist))
    except:
        print('初始化列表失败')
#把个人页面的名字和关注着的json 保存到数据库
def save2sql(name):
    person_url = 'https://www.zhihu.com'+name
    main_personal = session.get(person_url+'/following',headers=headers)
    soup = BeautifulSoup(main_personal.content,'html.parser')
    datalist = soup.find(id='Profile-following').find_all('div',attrs = {"class":"List-item"})
    print(name+'关注的列表长度'+str(len(datalist)))
    for listitem in datalist[0:]:
        #print(listitem.find('a',attrs={"class":"UserLink-link"}))
        #follow_name = (listitem.find('a',attrs={"class":"UserLink-link"})['href'])[8:]
        follow_name = listitem.find('a',attrs={"class":"UserLink-link"})['href']
        if follow_name in name_list:
            continue
        name_list.append(follow_name)
        time.sleep(1)
        pattern = re.compile(r'^/.+/(.+)')
        nopre_name=(pattern.findall(follow_name))[0]
        if nopre_name not in hasSavelist:
            time.sleep(1)
            person_json = session.get('https://www.zhihu.com/api/v4/members/'+nopre_name+'?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics',headers=headers)
            jsonstr = person_json.json()
            img_url = re.sub(r'{(.+)}','xl',jsonstr['avatar_url_template'])
            if jsonstr['gender']==0:
                gender = '女'
            elif jsonstr['gender']==1:
                gender = '男'
            else:
                gender = '未知'
            address = ''
            if len(jsonstr['locations'])>0:      #不知道为什么得到jsonstr['locations']后说是object，但是这里得到是列表
                address = jsonstr['locations'][0]['name']
            job_name = ''
            #if len(jsonstr['employments'])>0 and (jsonstr['employments'][0]).contain('job'):
            if len(jsonstr['employments'])>0:
                try:
                    job_name = jsonstr['employments'][0]['job']['name']
                except:
                    pass
            sql = "INSERT INTO zhihu_personal(username, whocareme,jobname,address,img_url,personaldetailurl,gender,headline,realname,answercount,articlescount,followingcount) VALUES('%s','%s','%s','%s','%s','%s' ,'%s','%s', '%s','%s','%s','%s')" % (nopre_name,name,job_name,address,img_url,person_url,gender,jsonstr['headline'],jsonstr['name'],str(jsonstr['answer_count']),str(jsonstr['articles_count']),str(jsonstr['following_count']))
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
                print("保存成功")
            except:
                print("保存失败")
                db.rollback()
                pass
        save2sql(follow_name)
def close_conn():
    db.close()
    
#运行
if __name__ == '__main__':
    hasSaveName()
    if isLogin():
        print('您已经登录')
    else:
        account = input('请输入你的用户名\n>  ')
        secret = input("请输入你的密码\n>  ")
        login(secret, account)
    account = input('请输入你的用户名\n>  ')
    secret = input("请输入你的密码\n>  ")
    login(secret, account)
    save2sql('/people/errorro0t')
    close_conn()

