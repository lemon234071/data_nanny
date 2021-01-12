import os
import json
import gzip
import tqdm


def sta_zhihu(dirpath):
    subdirs = [os.path.join(dirpath, x) for x in os.listdir(dirpath) if os.path.isdir(os.path.join(dirpath, x))]

    subsubdirs = [os.path.join(subdir, x) for subdir in subdirs for x in os.listdir(subdir) if
                  os.path.isdir(os.path.join(subdir, x))]
    cnt_fail = 0
    cnt_dialog = 0
    for subsubdir in tqdm.tqdm(subsubdirs):
        path = os.path.join(subsubdir, "zhihu")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                data = [json.loads(x) for x in f.readlines()]
        elif os.path.exists(path + ".gz"):
            with gzip.open(path, "rb", encoding="utf-8") as f:
                data = [json.loads(x) for x in f.readlines()]
        else:
            cnt_fail += 1
            print(subsubdir)
        print(data[0])
        print(subsubdir)
        cnt_dialog += len(data)
    print(cnt_fail, "failed")
    print("dialog:", cnt_dialog)


if __name__ == '__main__':
    sta_zhihu("/home/data/tripartite/aminer/yyq_scp/zhihu/")
