import os
import json
import gzip
import tqdm


def sta_zhihu(rootdirpath):
    # type dir: qa, comment, anwser
    subdirs = [os.path.join(rootdirpath, x) for x in os.listdir(rootdirpath) if
               os.path.isdir(os.path.join(rootdirpath, x))]

    # id dir: 7762
    subsubdirs = [os.path.join(subdir, x) for subdir in subdirs for x in os.listdir(subdir) if
                  os.path.isdir(os.path.join(subdir, x))]

    # date dir: 20181101
    subsubsubdirs = [os.path.join(subsubdir, x) for subsubdir in subsubdirs for x in os.listdir(subsubdir) if
                     os.path.isdir(os.path.join(subsubdir, x))]
    cnt_fail = 0
    cnt_dialog = 0
    for thisdir in tqdm.tqdm(subsubsubdirs):
        path = os.path.join(thisdir, "zhihu")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                data = [json.loads(x) for x in f.readlines()]
        elif os.path.exists(path + ".gz"):
            with gzip.open(path, "rb", encoding="utf-8") as f:
                data = [json.loads(x) for x in f.readlines()]
        else:
            cnt_fail += 1
            print(thisdir)
            continue
        print(data[0])
        print(thisdir)
        cnt_dialog += len(data)
    print(cnt_fail, "failed")
    print("dialog:", cnt_dialog)


if __name__ == '__main__':
    sta_zhihu("/home/data/tripartite/aminer/yyq_scp/zhihu/")
