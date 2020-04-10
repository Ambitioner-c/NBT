import numpy as np
import gensim.models as word2vec
import jieba
import re


# 设置卷积核
def set_cnn_filter(n_gram):
    array = np.random.rand(n_gram * 300, 300)

    return array


# 保存卷积核
def save_cnn_filter(path, array, n_gram):
    pathname = path + str(n_gram) + '_gram.npy'
    np.save(pathname, array)


# 获得卷积核
def get_cnn_filter(path, n_gram):
    pathname = path + str(n_gram) + '_gram.npy'
    array = np.load(pathname)

    return array


# 加载模型
def load_word2vec_model(model_path):
    model = word2vec.Word2Vec.load(model_path)
    return model


# 输出词向量
def get_vector(word, model):
    return model.wv.__getitem__(word)


# 增加专业名词
def set_user_dict(car_path):
    jieba.load_userdict(car_path)


# 获取结巴分词
def get_split(sentence):

    # 标点符号
    remove_chars = '[·’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'

    # 去除标点符号
    sentence = re.sub(remove_chars, "", sentence)

    # 分词
    words = [w for w in jieba.cut(sentence, cut_all=False)]

    return words


# relu函数
def relu(x):
    return np.where(x < 0, 0, x)


# max-polling函数
def poll(array):
    return array.max(axis=0)


def poll_sum(arrays):
    return arrays[0] + arrays[1] + arrays[2]


# 卷积神经网络
def nbt_cnn(sentence, model, cnn_filter_path, bs):
    # n-gram表征
    poll_arrays = []

    # 设置卷积核
    n_gram = 0
    for j in range(3):
        # n-gram
        n_gram += 1

        # 偏项
        b = bs[n_gram - 1]

        # 获取卷积核
        cnn_filter = get_cnn_filter(cnn_filter_path, n_gram)

        # 分词
        words = get_split(sentence)

        # 获得词向量
        vectors = []
        for k in words:
            vector = get_vector(k, model)
            vectors.append(vector)

        # 词向量
        words_vector = []

        # 1-gram
        if n_gram == 1:
            words_vector = vectors
        elif n_gram == 2:
            for k in range(len(vectors) - 1):
                gram = vectors[k].tolist()
                gram_1 = vectors[k + 1].tolist()
                gram.extend(gram_1)
                words_vector.append(np.asarray(gram))
        else:
            for k in range(len(vectors) - 2):
                gram = vectors[k].tolist()
                gram_1 = vectors[k + 1].tolist()
                gram_2 = vectors[k + 2].tolist()
                gram.extend(gram_1)
                gram.extend(gram_2)
                words_vector.append(np.asarray(gram))

        # 将句子向量转换成矩阵
        words_array = np.asarray(words_vector)

        # 卷积
        cnn_array = words_array.dot(cnn_filter)

        # 线性整流函数relu
        relu_array = relu(cnn_array + b)

        # 池化函数max-polling
        poll_array = poll(relu_array)
        poll_arrays.append(poll_array)

    # 语句表征
    r = poll_sum(poll_arrays)

    return r


if __name__ == '__main__':
    # 保存路径
    my_cnn_filter_path = '../../data/representation_data/'

    # # 设置卷积核
    # my_n_gram = 0
    # for i in range(3):
    #     # n-gram
    #     my_n_gram += 1
    #
    #     # 设置卷积核
    #     my_cnn_filter = set_cnn_filter(my_n_gram)
    #
    #     # 保存卷积核
    #     save_cnn_filter(my_cnn_filter_path, my_cnn_filter, my_n_gram)

    # 模型路径
    my_model_path = r'../../data/result_data/word2vec.model'

    # 加载模型
    my_model = load_word2vec_model(my_model_path)

    # 词向量
    # print_vector('奔驰')

    # 专业名词路径
    my_car_path = '../../data/jieba_data/car_name.txt'
    set_user_dict(my_car_path)

    # 句子
    my_sentence = '车快半年了，车内的味道还是很大。'

    # 偏项
    my_bs = [0.2, 0.3, 0.4]

    # 卷积神经网络
    my_r = nbt_cnn(my_sentence, my_model, my_cnn_filter_path, my_bs)
    print(my_r)
