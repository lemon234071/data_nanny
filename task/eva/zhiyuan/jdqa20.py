"""
京东客服对话数据
`/home/data/tripartite/zhiyuan/强语义数据/京东对话2020`
"""

import re
import numpy as np
from tqdm import tqdm
from utils import *

pattern = re.compile(r'(\S+)\s+fx\s+(\S+[\s\S]*)')


def iter_session(file_path: str):
    """
    :return:
        [
            {'role': '1' or '0', 'utt': ['t1', 't2']},
            {'role': '1' or '0', 'utt': ['t1']},
            {'role': '1' or '0', 'utt': ['t1', 't2', 't3']}
        ]
    """
    cur_session_id = ''
    cur_role = ''
    dialogue = []
    for line in tqdm(load_text_file_by_line(file_path), desc='process..'):
        try:
            session_id = line[:32]
            role = line[-1:]
            utt = line[38:-1].strip()
            if cur_session_id != session_id:
                cur_session_id = session_id
                if dialogue:
                    if len(dialogue) > 1:
                        yield dialogue
                    dialogue = []
                    cur_role = ''

            if cur_role != role:
                cur_role = role
                dialogue.append({'role': role, 'utt': []})

            dialogue[-1]['utt'].append(utt)
        except IndexError as e:
            print('[ERR] %s' % line)
    if dialogue and len(dialogue) > 1:
        yield dialogue


def count(dst_dir: str):
    num_session = 0
    num_sents = 0
    num_turns = []
    for file_path, file_name in find_cur_file_paths(dst_dir):
        if file_name.endswith('.txt'):
            print('File: ' + file_name)
            for session_dialogue in iter_session(file_path):
                num_session += 1
                num_sents += sum([len(t['utt']) for t in session_dialogue])
                num_turns.append(len(session_dialogue) // 2)
                # print(session_dialogue)
    print('sessions: %d' % num_session)
    print('sents: %d' % num_sents)
    print('avg turn: %f' % np.mean(num_turns))
    print('max turn: %d' % max(num_turns))
    print('min turn: %d' % min(num_turns))


if __name__ == '__main__':
    import sys

    dst_dir = '/home/data/tripartite/zhiyuan/强语义数据/京东对话2020'
    # dst_dir = '/home/one/PycharmProjects/data_nanny/data/京东对话2020'
    if len(sys.argv) >= 2:
        dst_dir = sys.argv[1]
    count(dst_dir)

    """
    sessions: 221487
    sents: 4969780
    avg turn: 6.985047
    max turn: 149
    min turn: 1
    """
