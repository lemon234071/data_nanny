"""
cmedqa
`/home/data/tripartite/zhiyuan/强语义数据/medqa/cMedQA2`
"""
from utils import *


def count(file_path_a: str, file_path_q: str):
    df_a = load_pandas_file(file_path_a)
    df_q = load_pandas_file(file_path_q)
    num_session = len(df_a)
    num_sents = len(df_a) + len(df_q)
    print('sessions: %d' % num_session)
    print('sents: %d' % num_sents)
    print('avg turn: %f' % 1)
    print('max turn: %d' % 1)
    print('min turn: %d' % 1)


if __name__ == '__main__':
    import sys

    file_path_a = '/home/data/tripartite/zhiyuan/强语义数据/medqa/cMedQA2/answer.csv'
    file_path_q = '/home/data/tripartite/zhiyuan/强语义数据/medqa/cMedQA2/question.csv'
    # file_path_a = '/home/one/PycharmProjects/data_nanny/data/medqa/cMedQA2/answer.csv'
    # file_path_q = '/home/one/PycharmProjects/data_nanny/data/medqa/cMedQA2/question.csv'
    if len(sys.argv) >= 3:
        file_path_a = sys.argv[1]
        file_path_q = sys.argv[1]
    count(file_path_a, file_path_q)

    """
    sessions: 226266
    sents: 346266
    avg turn: 1.000000
    max turn: 1
    min turn: 1
    """
