# -*- coding:utf-8 -*-
import requests
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import re
import csv
from time import sleep
from random import randint


class ParseHtml(object):
    def __init__(self):
        self.header = {"host": "k.autohome.com.cn",
                       "user-agent": "Mozilla/5.0 (X11; Linux x86_64)"
                                     " AppleWebKit/537.36 (KHTML, like Gecko)"
                                     " Chrome/80.0.3987.106 Safari/537.36",
                       "accept": "text/html,application/xhtml+xml,application/xml;"
                                 "q=0.9,image/webp,image/apng,*/*;"
                                 "q=0.8,application/signed-exchange;"
                                 "v=b3;"
                                 "q=0.9",
                       "accept-language": "zh-CN,zh;q=0.9",
                       "accept-encoding": "gzip, deflate, br",
                       "connection": "keep-alive",
                       "upgrade-insecure-requests": "1",
                       "referer": "https://m.autohome.com.cn/3170/"}

    @staticmethod
    def get_html_doc(url):
        """根据传入的url,获得所有口碑页面的html代码"""
        s = requests.Session()
        resp = s.get(url, verify=False)
        if resp.status_code != 200:
            return 'Error'
        else:
            return resp.content

    @staticmethod
    def get_text_con(html_doc):
        """解析网页源代码,利用css属性,获得口碑内容部分的源代码"""
        soup = BeautifulSoup(html_doc, 'lxml')
        mouth_matter = soup.find_all(class_='matter')[-1:][0]
        return mouth_matter

    @staticmethod
    def get_font_url(html_doc):
        """利用正则获取字体文件链接"""
        font_url = re.findall(r'\w+\.\w+\..*?ttf', html_doc)[0]
        return font_url


def run(mouth_id):
    url = "https://k.m.autohome.com.cn/detail/view_" + mouth_id + ".html"

    parse = ParseHtml()

    # 获得网页源代码
    html_doc = parse.get_html_doc(url)

    # 网络异常判断
    if html_doc == 'Error':
        return 'Error', 'Error'
    else:
        text_con = parse.get_text_con(html_doc)
        font_text = text_con.text.replace('\n', '').replace(' ', '')

        font_url = ''
        if html_doc == 1:
            run(url)
        else:
            # 获取字体文件链接
            font_url = parse.get_font_url(bytes.decode(html_doc, encoding='utf-8'))

    return font_text, font_url


def schedule(a, b, c):
    # a:已经下载的数据块
    # b:数据块的大小
    # c:远程文件的大小
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('%.2f%%' % per)


def download(font_text, font_url, download_path, mouth_id):
    text_path = download_path + mouth_id + '.txt'
    with open(text_path, 'w') as f:
        f.write(font_text)

    font_path = download_path + mouth_id + '.ttf'
    urlretrieve('http://' + font_url, font_path)


def get_show_id(car_id, show_id_path):
    all_show_id = []
    reader = csv.reader(open(show_id_path, 'r'))
    for j in reader:
        if j[0] == car_id:
            all_show_id.append(j[1])

    return all_show_id


if __name__ == '__main__':
    # 车id
    my_car_id = '4851'

    # 展示id路径
    my_show_id_path = '../../../../data/mouth_spider/show_id.csv'

    # 获得该车的全部展示id
    my_all_show_id = get_show_id(my_car_id, my_show_id_path)

    for i in range(len(my_all_show_id)):
        sleep(randint(5, 8))

        # id
        my_mouth_id = my_all_show_id[i]
        my_url = 'https://k.m.autohome.com.cn/detail/view_' + my_all_show_id[i] + '.html'

        # 保存路径
        my_download_path = r'../../../../data/mouth_spider/mouth_data/'
        my_font_text, my_font_url = run(my_mouth_id)

        # 网络异常处理
        if my_font_text == 'Error':
            print('网络异常，休眠20s')
            sleep(randint(10, 15))

            continue
        else:

            download(my_font_text, my_font_url, my_download_path, my_mouth_id)

            # 显示进度
            schedule(i, 1, len(my_all_show_id))
