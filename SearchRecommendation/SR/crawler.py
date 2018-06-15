#_*_ coding:utf-8 _*_
import requests
import random
import time
import socket
import http.client
from bs4 import BeautifulSoup

def get_content(url):
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url,headers = header,timeout = timeout)
            rep.encoding = 'utf-8'
            break
        except socket.timeout as e:
            print( '1:', e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print( '2:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print( '3:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print( '4:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text

def get_contentbyindex(index, dd):
    if dd[index].find('a') is None:
        content = dd[index].string.replace('\n', '')
    else:
        staring = dd[index].contents[0]
        a = dd[index].find_all('a')
        for _a in a:
            staring += _a.string.replace('\n', '') + ','
        content = staring
    return content

def get_data(html_text):
    try:
        item = {'writer': '', 'staring': '', 'style': '', 'picture': ''}
        bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
        body = bs.body  # 获取body部分

        imgsrc = get_img(body)  # 获取海报图片地址
        item['picture'] = imgsrc

        data = body.find('div', {'class': 'basic-info cmn-clearfix'})  # 找到class为basic-info cmn-clearfix的div
        dl = data.find_all('dl')  # 获取dl部分

        print(len(dl))
        for _dl in dl:
            dd = _dl.find_all('dd')  # 获取所有的dd
            dt = _dl.find_all('dt')

            for index in range(len(dd)):
                propertyname = str(dt[index].string)
                print(propertyname)
                content = get_contentbyindex(index, dd)
                if propertyname == "编    剧" or propertyname == "作    者":
                    item["writer"] = content
                elif dt[index].string == "主    演":
                    item["staring"] = content
                elif dt[index].string == "类    型":
                    item["style"] = content
    except:
        print("出现异常")
    return item

def get_img(body):
    try:
        div = body.find('div', {'class': 'main-content'})
        img = div.find('img')
        imgsrc = img['src']
    except:
        imgsrc = ''
    return imgsrc



def get_infor(publationname):
    url = "https://baike.baidu.com/item/" + publationname
    html = get_content(url)
    return get_data(html)
