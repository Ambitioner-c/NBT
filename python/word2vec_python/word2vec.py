import gensim.models as word2vec
from gensim.models.word2vec import LineSentence


# 训练词向量
# corpus_path：语料库路径，vector_path：词向量保存路径，model_path：模型保存路径
def train_word2vec(corpus_path, vector_path, model_path):
    # 把语料变成句子集合
    sentences = LineSentence(corpus_path)

    # 训练word2vec模型（size为向量维度，window为词向量上下文最大距离，min_count需要计算词向量的最小词频）
    # (iter随机梯度下降法中迭代的最大次数，sg为3是Skip-Gram模型)
    model = word2vec.Word2Vec(sentences, size=300, sg=3, window=5, min_count=1, workers=10, iter=10)

    # 保存word2vec模型
    model.save(model_path)
    model.wv.save_word2vec_format(vector_path, binary=False)


# 加载模型
def load_word2vec_model(model_path):
    model = word2vec.Word2Vec.load(model_path)
    return model


# 计算词语最相似的词
def calculate_most_similar(model, word):
    similar_words = model.wv.most_similar(word)
    print(word)
    for j in similar_words:
        print(j[0], j[1])


# 计算两个词相似度
def calculate_words_similar(model, word1, word2):
    print(model.similarity(word1, word2))


# 找出不合群的词
def find_word_dis_match(model, lists):
    print(model.wv.doesnt_match(lists))


if __name__ == '__main__':
    # 语料库路径
    my_corpus_path = r'../../data/result_data/corpus.txt'
    # 语料向量路径
    my_vector_path = r'../../data/result_data/corpus.vector'
    # 模型路径
    my_model_path = r'../../data/result_data/word2vec.model'

    # # 训练模型
    # train_word2vec(my_corpus_path, my_vector_path, my_model_path)

    # 加载模型
    my_model = load_word2vec_model(my_model_path)

    # # 找相近词
    # calculate_most_similar(my_model, "奥迪")

    # # 两个词相似度
    # calculate_words_similar(my_model, "奥迪", "德国")

    # 词向量
    print(my_model.wv.__getitem__('奔驰'))

    # # 找不同
    # my_lists = ["奔驰", "奥迪", "大众", "比亚迪"]
    # find_word_dis_match(my_model, my_lists)
