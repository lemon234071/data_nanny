import os
import tqdm
import collections

from data_utils import *


def check_zhihu_id(rootdirpath, file_name, sta_dir):
    #
    qest_dict = collections.defaultdict(int)
    ans_dict = collections.defaultdict(int)
    com_dict = collections.defaultdict(int)
    no_id = 0
    two_id = 0

    # type dialog
    types = [x for x in os.listdir(rootdirpath) if not x.endswith("tar.gz")]
    failed_file = []
    for data_type in types:
        filedirs = [os.path.join(rootdirpath, data_type)]
        # go down to the dir
        while not [x for x in os.listdir(filedirs[0]) if ".gz" in x]:
            filedirs = [os.path.join(subdir, x)
                        for subdir in filedirs
                        for x in os.listdir(subdir)
                        if os.path.isdir(os.path.join(subdir, x))]

        for thisdir in tqdm.tqdm(filedirs):
            path = os.path.join(thisdir, file_name)
            try:
                if os.path.exists(path):
                    data = load_jsonl(path)
                elif os.path.exists(path + ".gz"):
                    data = load_gz_jsonl(path + ".gz")
                else:
                    print("wrong data type", thisdir)
                    continue

                for line in data:
                    # if "qid" not in line.keys() and "pid_str" not in line.keys():
                    #     no_id += 1
                    #     continue
                    # if "qid" in line and "pid_str" in line and str(line["qid"]) != str(line["pid_str"]):
                    #     two_id += 1
                    #     continue
                    #
                    # id_k = "qid" if "qid" in line else "pid_str"
                    # id = str(line[id_k])

                    if "url" not in line:
                        no_id += 1

                    url = line["url"]
                    url = url[url.find("www.zhihu.com/question/") + 23:]
                    if "/" in url:
                        url = url[:url.find("/")]
                    id = url

                    if data_type == "qa":
                        qest_dict[id] += 1
                    elif data_type == "answer":
                        ans_dict[id] += 1
                    else:
                        com_dict[id] += 1

            except Exception as e:
                failed_file.append(thisdir)
                print(e)
        print("failed_file:", failed_file)

    sta = {
        "question number": len(qest_dict.keys()),
        "answer number": len(ans_dict.keys()),
        "comment number": len(com_dict.keys()),
        "qest_wo_ans": len(set(qest_dict.keys()) - set(ans_dict.keys())),
        "qest_wo_com": len(set(qest_dict.keys()) - set(com_dict.keys())),
        "no_id": no_id,
        "two_id": two_id
    }
    print(sta)
    sta.update({"qest": qest_dict, "ans": ans_dict, "com": com_dict})
    save_json(sta, os.path.join(sta_dir, "check_zhihu_urlid.json"))
    print("check id over", file_name)
    return


if __name__ == '__main__':
    check_zhihu_id("/extension/wangyida/data/dialog/zh/tripartite/aminer/yyq_scp/zhihu/", "zhihu",
                   "/extension/wangyida/data/dialog/zh/tripartite/aminer/yyq_scp/sta/")
