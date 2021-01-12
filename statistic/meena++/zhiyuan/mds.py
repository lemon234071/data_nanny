import re
from .utils import *


def iter_session_org_text(file_path):
    ret = ''
    for line in load_text_file_by_line(file_path):
        if line.startswith('id='):
            if ret:
                yield ret
                ret = ''
        else:
            ret += line + '\n'


pattern = re.compile(r'Dialogue\n([\s\S]*)')


def get_dialogue(session_org_text: str):
    dialogue = []
    obj = pattern.search(session_org_text)
    if obj is not None:
        lines = obj.group(1).split('\n')
        role = ''
        for line in lines:
            if line.startswith('真情寄语：'):
                continue
            if line.startswith('医生：') or line.startswith('病人：'):
                new_role = line[:2]
                if new_role == role:
                    dialogue[-1]['utt'] += line
                else:
                    role = new_role
                    dialogue.append({'role': role, 'utt': ''})
            elif role:
                dialogue[-1]['utt'] += line

    return [turn for turn in dialogue if turn['utt']]


def iter_dialogue(file_paths: list):
    for file_path in file_paths:
        print(file_path)
        for session_org_text in iter_session_org_text(file_path):
            yield get_dialogue(session_org_text)


if __name__ == '__main__':
    file_paths = ['2010.txt', '2011.txt', '2013.txt', '2014.txt']
    dialogues = [dialogue for dialogue in iter_dialogue(file_paths)]
    print('')
