"""
中文医疗对话数据集
`/home/data/tripartite/zhiyuan/强语义数据/6个科室的问答数据`
['department' 'title' 'ask' 'answer']
"""
from utils import *


def count(dst_dir: str):
    num_session = 0
    num_sents = 0
    for file_path, file_name in find_all_file_paths(dst_dir):
        if file_name.endswith('.csv') and '样例' not in file_name:
            print('File: ' + file_name)
            df = load_pandas_file(file_path)
            num_session += len(df)
            num_sents += len(df) * 2
    print('sessions: %d' % num_session)
    print('sents: %d' % num_sents)
    print('avg turn: %f' % 1)
    print('max turn: %d' % 1)
    print('min turn: %d' % 1)


if __name__ == '__main__':
    import sys

    dst_dir = '/home/data/tripartite/zhiyuan/强语义数据/6个科室的问答数据/Data_数据'
    # dst_dir = '/home/one/PycharmProjects/data_nanny/data/6个科室的问答数据/Data_数据'
    if len(sys.argv) >= 2:
        dst_dir = sys.argv[1]
    count(dst_dir)

    """
    sessions: 792099
    sents: 1584198
    avg turn: 1.000000
    max turn: 1
    min turn: 1
    """
