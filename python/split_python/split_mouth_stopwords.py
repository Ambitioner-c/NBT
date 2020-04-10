import jieba
import jieba.posseg as jp


# 获取停用词
def get_stopwords(stopwords_path):
    # 停用词列表
    stopwords = []
    with open(stopwords_path, 'r', encoding='utf-8') as f:

        lines = f.readlines()
        for j in lines:
            line = j.replace('\n', '')
            stopwords.append(line)

    return stopwords


# 获取结巴分词
# file_path：语料库路径，stopwords：停用词列表，car_path：自定义语料库路径，flags：词性，corpus_path：保存路径
def get_split(file_path, stopwords, car_path, flags, corpus_path):
    split = ''

    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()

        # 增加专业名词
        jieba.load_userdict(car_path)
        words = [w.word for w in jp.cut(txt) if w.flag in flags and w.word not in stopwords]
        text = ' '.join(words)
        split += text

    with open(corpus_path, 'w', encoding='utf-8') as f:
        f.write(split)


if __name__ == '__main__':
    # 停用词路径
    my_stopwords_path = r'../../data/jieba_data/stopwords.txt'
    # 源数据路径
    my_file_path = r'../../data/mouth_spider/mouth.txt'
    # 专业名词路径
    my_car_path = r'../../data/jieba_data/car_name.txt'
    # 语料库路径
    my_corpus_path = r'../../data/result_data/corpus_stopwords.txt'

    # 词性
    # 名词、地名、机构团体、英文、动词、形容词
    my_flags = ('n', 'ns', 'nt', 'eng', 'v', 'a')

    # 获取停用词
    my_stopwords = get_stopwords(my_stopwords_path)

    # 分词
    get_split(my_file_path, my_stopwords, my_car_path, my_flags, my_corpus_path)
