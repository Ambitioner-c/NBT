import requests
import json
from time import sleep
from random import randint
import csv


Headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64)"
                         " AppleWebKit/537.36 (KHTML, like Gecko)"
                         " Chrome/80.0.3987.106 Safari/537.36",
           }


def schedule(a, b, c):
    # a:已经下载的数据块
    # b:数据块的大小
    # c:远程文件的大小
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print('当前进度：%.2f%%' % per)


def spider(car_id):
    # 该车的所有展示id
    all_show_id = []

    show_id, page_count = get_show_id(car_id)
    all_show_id.extend(show_id)

    for j in range(2, page_count):
        sleep(randint(2, 5))
        show_id, page_count = get_show_id(car_id, j)
        all_show_id.extend(show_id)

    # 显示进度
    schedule(page_count, 20, page_count * 20)

    return all_show_id


def get_show_id(car_id, page=1):
    # 当前页的展示id
    show_id = []

    url = 'https://k.m.autohome.com.cn/ajax/series/getserieskoubeilist' \
          '?pageIndex=' + str(page) +  \
          '&isSeries=true' \
          '&Id=' + car_id + \
          '&SemanticKey=' \
          '&IsSemantic=false' \
          '&GradeEnum=0' \
          '&order=1' \
          '&yearId=0' \
          '&provinceId=110000' \
          '&summarykey=0' \
          '&isSending=true'

    html = requests.get(url, headers=Headers)
    html_json = json.loads(html.text)

    # 页面总数
    page_count = html_json['result']['pagecount']

    # 获取当前页的全部是show id
    for j in html_json['result']['list']:
        show_id.append(j['showId'])

    # 显示进度
    schedule(page, 20, page_count*20)

    return show_id, page_count


def write(car_id, all_show_id, path):
    with open(path, 'w') as f:
        f_writer = csv.writer(f)

        for j in range(len(all_show_id)):
            f_writer.writerow([car_id,
                               all_show_id[j]])


if __name__ == '__main__':
    # 保存路径
    my_path = '../../../../data/mouth_spider/show_id.csv'

    # 车id
    my_car_id = '4851'

    # 获取全部展示id
    my_all_show_id = spider(my_car_id)

    # 保存
    write(my_car_id, my_all_show_id, my_path)
