
def load_text_file_by_line(file_path):
    with open(file_path, 'r', encoding='UTF-8') as f:
        data = [token.replace('\n', '').replace('\r', '') for token in f.readlines()]
    return [x for x in data if x]
