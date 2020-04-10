import jieba
import re


# 获取结巴分词
def get_split(file_path, car_path):
    split = ''

    # 标点符号
    remove_chars = '[·’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'

    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()
        # 去除标点符号
        txt = re.sub(remove_chars, "", txt)

        # 增加专业名词
        jieba.load_userdict(car_path)
        words = [w for w in jieba.cut(txt, cut_all=False)]
        text = ' '.join(words)
        split += text

    return split


def write(corpus_path, split):
    with open(corpus_path, 'w', encoding='utf-8') as f:
        f.write(split)


if __name__ == '__main__':
    # 源数据路径
    my_file_path = r'../../data/mouth_spider/mouth.txt'
    # 专业名词路径
    my_car_path = r'../../data/jieba_data/car_name.txt'
    # 语料库路径
    my_corpus_path = r'../../data/result_data/corpus.txt'

    # 分词
    my_split = get_split(my_file_path, my_car_path)

    # 保存
    write(my_corpus_path, my_split)
