from fontTools.ttLib import TTFont


def parse_ttf(download_path, mouth_id):
    # 解析字体库
    font = TTFont(download_path + mouth_id + '.ttf')

    # 读取字体的映射关系
    uni_list = font['cmap'].tables[0].ttFont.getGlyphOrder()

    # 转换格式
    utf_list = [eval(r"u'\u" + x[3:] + "'") for x in uni_list[1:]]

    return utf_list


def replace(utf_list, text):
    # 被替换的字体的列表
    word_list = [u'着', u'机', u'好', u'九', u'左', u'路', u'远', u'上', u'动', u'门',
                 u'副', u'档', u'真', u'了', u'小', u'短', u'实', u'盘', u'大', u'坏', u'空',
                 u'右', u'五', u'油', u'软', u'是', u'二', u'外', u'十', u'得', u'泥', u'地',
                 u'呢', u'音', u'控', u'保', u'手', u'光', u'启', u'四', u'养', u'七', u'不',
                 u'冷', u'味', u'的', u'矮', u'一', u'只', u'低', u'孩', u'有', u'来', u'和',
                 u'高', u'灯', u'自', u'耗', u'开', u'身', u'多', u'内', u'三', u'下', u'量',
                 u'硬', u'长', u'雨', u'八', u'排', u'皮', u'很', u'过', u'更', u'响', u'少',
                 u'坐', u'当', u'里', u'比', u'加', u'六', u'近', u'无', u'性', u'中', u'问',
                 u'级', u'公', u'电']

    # 遍历需要被替换的字符
    for i in range(len(utf_list)):
        text = text.replace(utf_list[i], word_list[i])

    return text


def read_txt(download_path, mouth_id):
    with open(download_path + mouth_id + '.txt', 'r') as f:
        text = f.read()

    return text


if __name__ == '__main__':
    # id
    my_mouth_id = '01cjv944pg68rk2d9p6wr00000'

    # 保存路径
    my_download_path = r'../../../../data/mouth_spider/mouth_data/'

    # 解析ttf文件
    my_utf_list = parse_ttf(my_download_path, my_mouth_id)
    print(my_utf_list)

    # 读取原文档
    old_text = read_txt(my_download_path, my_mouth_id)

    # 替换为新文档
    new_text = replace(my_utf_list, old_text)

    print(new_text)
