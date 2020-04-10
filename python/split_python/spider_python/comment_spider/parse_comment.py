import csv
import demjson
import os


# 递归找到对话链
def recursion(obj, chain=None, floor=-1):
    # 评论可能删除
    if obj.get(floor):
        if obj[floor][1] != -1:
            # 添加链条
            chain.append(floor)

            # 递归
            recursion(obj, chain, floor=obj[floor][1])
        else:
            # 添加链条
            chain.append(floor)
    else:
        pass

    return chain


def get_comment_file(dirs_path):
    # 文件名列表
    files = []

    dirs = os.listdir(dirs_path)
    for j in dirs:
        files.append(j)

    return files


# 解析评论数据
def parse_test(file, min_count):
    path = '../../../../data/comment_spider/comment_data/' + str(file)
    print('当前文夹{0}'.format(file))

    # 汽车id
    car_id = ''
    # 口碑id
    mouth_id = ''
    # 作者id
    author_id = ''
    # 全部可用评论
    comments = []

    reader = csv.reader(open(path, 'r'))
    for j in reader:
        car_id = j[0]
        mouth_id = j[1]
        author_id = j[2]
        # 评论总数
        comment_num = int(j[3])

        # 评论总数至少有min_count条
        if comment_num >= min_count:
            # 评论字典
            comment_dict = j[4]

            # 因为存在数字，所以改用demjson
            comment_json = demjson.decode(comment_dict)

            # 楼层链
            floor_chains = []
            # 已经记录的楼层链
            floor_chained = []
            for k in comment_json:
                if k not in floor_chained:
                    # 递归
                    floor_chain = recursion(obj=comment_json, chain=[], floor=k)

                    # 已经记录的楼层
                    floor_chained.extend(floor_chain)

                    # 保存
                    if len(floor_chain) >= min_count:
                        floor_chains.append(floor_chain)

            # 评论链
            comment_chains = []
            for k in floor_chains:
                comment_chain = []

                # 反向楼层链
                k.reverse()
                for m in k:
                    comment_chain.append(comment_json[m][0])
                comment_chains.append(comment_chain)

            if len(comment_chains) != 0:
                comments.append(comment_chains)

    return car_id, mouth_id, author_id, comments


# 保存评论
def write(comment_path,
          car_id, mouth_id, author_id,
          comment_chains):

    with open(comment_path, 'a') as f:
        f_writer = csv.writer(f)

        for j in comment_chains:
            f_writer.writerow([car_id, mouth_id, author_id,
                               j[0]])


if __name__ == '__main__':
    # 评论文件夹路径
    my_dirs_path = '../../../../data/comment_spider/comment_data/'

    # 对话最少评论
    my_min_count = 10

    # 保存路径
    my_comment_path = '../../../../data/comment_spider/comment_' \
                      + str(my_min_count) \
                      + '.csv'

    # 获取文件夹下文件名
    my_files = get_comment_file(my_dirs_path)

    for i in my_files:
        # 解析评论数据
        my_car_id, my_mouth_id, my_author_id, my_comment_chains = parse_test(i, my_min_count)

        # 保存评论
        write(my_comment_path,
              my_car_id, my_mouth_id, my_author_id,
              my_comment_chains)
