#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import numpy as np
from tqdm import tqdm
from utils import *

pattern = re.compile(r'(\S+)\s+(\S+)\s+([QA])\s+(.*)')


def iter_session(file_path: str):
    """
    :return:
        [
            {'role': 'Q' or 'A', 'utt': ['t1', 't2']},
            {'role': 'Q' or 'A', 'utt': ['t1']},
            {'role': 'Q' or 'A', 'utt': ['t1', 't2', 't3']}
        ]
    """
    cur_session_id = ''
    cur_role = ''
    dialogue = []
    for line in tqdm(load_text_file_by_line(file_path)[1:], desc='load chunk file'):
        obj = pattern.search(line)
        if obj is not None:
            session_id = obj.group(1)
            role = obj.group(3)
            utt = obj.group(4)
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
        else:
            print('[ERR] %s' % line)
    if dialogue and len(dialogue) > 1:
        yield dialogue


def count(file_path: str):
    num_session = 0
    num_sents = 0
    num_turns = []
    for session_dialogue in iter_session(file_path):
        num_session += 1
        num_sents += sum([len(t['utt']) for t in session_dialogue])
        num_turns.append(len(session_dialogue) // 2)

    print('sessions: %d' % num_session)
    print('sents: %d' % num_sents)
    print('avg turn: %f' % np.mean(num_turns))
    print('max turn: %d' % max(num_turns))
    print('min turn: %d' % min(num_turns))


if __name__ == '__main__':
    import sys

    file_path = '/home/data/tripartite/zhiyuan/强语义数据/京东对话2019数据集/JDDC_Dataset_LREC.txt'
    # file_path = '/Users/lixiang/PycharmProjects/data_nanny/data/京东对话2019数据集/JDDC_Dataset_LREC.txt'
    if len(sys.argv) >= 2:
        file_path = sys.argv[1]
    count(file_path)

    '''
    sessions: 1023843
    sents: 20450436
    avg turn: 6.356513
    max turn: 37
    min turn: 1
    '''
