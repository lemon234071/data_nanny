"""
好大夫中文医疗问答数据
"""

import re
import numpy as np
from utils import *


def iter_session_org_text(file_path):
    ret = ''
    for line in load_text_file_by_line(file_path):
        if line.startswith('id='):
            if ret:
                yield ret
                ret = ''
        else:
            ret += (line + '\n')
    if ret:
        yield ret


SECTION_NAMES = ['Doctor faculty', 'Description', 'Dialogue', 'Diagnosis and suggestions']


def get_sections_text(session_org_text: str):
    ret = {name: '' for name in SECTION_NAMES}
    cur_section = ''
    for line in session_org_text.split('\n'):
        if line.startswith('Doctor faculty'):
            cur_section = 'Doctor faculty'
        elif line.startswith('Description'):
            cur_section = 'Description'
        elif line.startswith('Dialogue'):
            cur_section = 'Dialogue'
        elif line.startswith('Diagnosis and suggestions'):
            cur_section = 'Diagnosis and suggestions'
        elif cur_section and line:
            ret[cur_section] += (line + '\n')
    return ret


def turn_to_dialogue(dialogue_text: str):
    dialogue = []
    role = ''
    for line in dialogue_text.split('\n'):
        if line.startswith('真情寄语：'):
            continue
        if line.startswith('医生：') or line.startswith('病人：'):
            new_role = line[:2]
            if not new_role == role:
                role = new_role
                dialogue.append({'role': role, 'utt': ''})
        elif role:
            dialogue[-1]['utt'] += line

    return [turn for turn in dialogue if turn['utt']]


def iter_session(file_path: str):
    """
    :return:
        [
            {'role': '医生' or '病人', 'utt': 'xxxxxx'},
            {'role': '医生' or '病人', 'utt': 'xxxxxx'},
            {'role': '医生' or '病人', 'utt': 'xxxxxx'}
        ]
    """
    for session_org_text in iter_session_org_text(file_path):
        dialogue_text = get_sections_text(session_org_text).get('Dialogue', '')
        session_dialogue = turn_to_dialogue(dialogue_text)
        if len(session_dialogue) > 1:
            yield session_dialogue


def count(dst_dir: str):
    num_session = 0
    num_sents = []
    num_turns = []
    for file_path, file_name in find_cur_file_paths(dst_dir):
        if '.txt' in file_name:
            print('File: ' + file_name)
            for session_dialogue in iter_session(file_path):
                num_session += 1
                num_sents.append(len(session_dialogue))
                num_turns.append(len(session_dialogue) // 2)
                # print(session_dialogue)
    print('sessions: %d' % num_session)
    print('sents: %d' % len(num_sents))
    print('avg sent len: %f' % np.mean(num_sents))
    print('max sent len: %d' % max(num_sents))
    print('min sent len: %d' % min(num_sents))
    print('avg turn: %f' % np.mean(num_turns))
    print('max turn: %d' % max(num_turns))
    print('min turn: %d' % min(num_turns))


if __name__ == '__main__':
    import sys

    dst_dir = '/home/data/tripartite/zhiyuan/强语义数据/中文医疗问答数据-好大夫/中文医疗问答数据-好大夫'
    if len(sys.argv) >= 2:
        dst_dir = sys.argv[1]
    count(dst_dir)
    '''
    sessions: 1037649
    sents: 1037649
    avg sent len: 4.425898
    max sent len: 507
    min sent len: 2
    avg turn: 1.893625
    max turn: 253
    min turn: 1
    '''
