import jieba
import re
import os
import csv
import demjson


def get_comment_file(dirs_path):
    # 文件名列表
    files = []

    dirs = os.listdir(dirs_path)
    for j in dirs:
        files.append(j)

    return files


# 获取结巴分词
def get_split(file_path, car_path, corpus_path):
    # 分词结果
    split = ''

    # 一种车下的所有评论
    comments = ''

    # 标点符号
    remove_chars = '[·’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'

    reader = csv.reader(open(file_path, 'r', encoding='utf-8'))
    for j in reader:
        # 评论总数
        comment_num = int(j[3])

        # 一个口碑下的所有评论
        comment = ''

        # 评论总数至少有min_count条
        if comment_num >= 1:
            # 评论字典
            comment_dict = j[4]

            # 因为存在数字，所以改用demjson
            comment_json = demjson.decode(comment_dict)
            for k in comment_json:
                comment += comment_json[k][0]
        comments += comment

    # 分词
    # 去除标点符号
    txt = re.sub(remove_chars, "", comments)

    # 增加专业名词
    jieba.load_userdict(car_path)
    words = [w for w in jieba.cut(txt, cut_all=False)]
    text = ' '.join(words)
    split += text

    with open(corpus_path, 'a', encoding='utf-8') as f:
        f.write(split)


if __name__ == '__main__':
    # 评论文件夹路径
    my_dirs_path = '../../data/comment_spider/comment_data/'

    # 获取文件夹下文件名
    my_files = get_comment_file(my_dirs_path)

    for i in my_files:
        # 源数据路径
        my_file_path = r'../../data/comment_spider/comment_data/' + i
        # 专业名词路径
        my_car_path = r'../../data/jieba_data/car_name.txt'
        # 语料库路径
        my_corpus_path = r'../../data/result_data/corpus_stopwords.txt'

        # 分词
        get_split(my_file_path, my_car_path, my_corpus_path)
