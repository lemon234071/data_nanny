import os
import sys
import json
import gzip
import tqdm
import collections


def count_dialog(rootdirpath, file_name):
    # type dialog
    types = os.listdir(rootdirpath)
    cnt_typs = collections.defaultdict(int)
    failed_file = []
    for data_type in types:
        filedirs = [os.path.join(rootdirpath, data_type)]
        while not [x for x in os.listdir(filedirs[0]) if file_name in x]:
            filedirs = [os.path.join(subdir, x) for subdir in filedirs for x in os.listdir(subdir) if
                        os.path.isdir(os.path.join(subdir, x))]

        for thisdir in tqdm.tqdm(filedirs):
            path = os.path.join(thisdir, file_name)
            try:
                if os.path.exists(path):
                    with open(path) as f:
                        for x in f.readlines():
                            if x.strip():
                                try:
                                    line = json.loads(x)
                                    cnt_typs[data_type] += 1
                                except:
                                    cnt_typs[data_type + "_failed_line"] += 1
                elif os.path.exists(path + ".gz"):
                    with gzip.open(path + ".gz", "rb") as f:
                        for x in f.readlines():
                            if x.strip():
                                try:
                                    line = json.loads(x)
                                    cnt_typs[data_type] += 1
                                except:
                                    cnt_typs[data_type + "_failed_line"] += 1
                else:
                    cnt_typs["wrong_file_type"] += 1
                    print("wrong data type", thisdir)
                    continue
            except:
                failed_file.append(thisdir)
                continue
        print(cnt_typs)
        print("failed_file:", failed_file)
    print("statistic over", file_name)




if __name__ == '__main__':
    # "/home/data/tripartite/aminer/yyq_scp/zhihu/", "zhihu"
    # "/home/data/tripartite/aminer/yyq_scp/baidu/", "baidu"
    count_dialog(sys.argv[1], sys.argv[2])
