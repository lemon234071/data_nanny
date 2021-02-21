import os
import tqdm
import collections

from data_utils import *


def debug_qid(id_path, urlid_path, rootdirpath, outpath):
    # uid = load_json(id_path)
    # url_uid = load_json(urlid_path)
    #
    # questions = (set(uid["qest"]) & set(uid["ans"])) | (set(uid["qest"]) & set(uid["com"]))
    # url_questions = (set(url_uid["qest"]) & set(url_uid["ans"])) | (
    #         set(url_uid["qest"]) & set(url_uid["com"]))
    # questions = {k: set() for k in questions}
    # url_questions = {k: set() for k in url_questions}
    # print(len(questions), "len question")
    # print(len(url_questions), "len url question")
    questions = collections.defaultdict(set)
    url_questions = collections.defaultdict(set)

    # type dialog
    types = [x for x in os.listdir(rootdirpath) if not x.endswith("tar.gz")]
    failed_file = []
    for data_type in types:
        #
        if data_type != "qa":
            continue

        filedirs = [os.path.join(rootdirpath, data_type)]
        # go down to the dir
        while not [x for x in os.listdir(filedirs[0]) if ".gz" in x]:
            filedirs = [os.path.join(subdir, x)
                        for subdir in filedirs
                        for x in os.listdir(subdir)
                        if os.path.isdir(os.path.join(subdir, x))]

        for thisdir in tqdm.tqdm(filedirs):
            path = os.path.join(thisdir, "zhihu")
            try:
                if os.path.exists(path):
                    data = load_jsonl(path)
                elif os.path.exists(path + ".gz"):
                    data = load_gz_jsonl(path + ".gz")
                else:
                    print("wrong data type", thisdir)
                    continue

                for line in data:
                    if "content" not in line:
                        continue

                    content = line["content"]
                    # idstr = "" if "idstr" not in line else line["idstr"]

                    if "qid" in line.keys() or "pid_str" in line.keys():
                        id_k = "qid" if "qid" in line else "pid_str"
                        uid = str(line[id_k])
                        # if uid in questions:
                        questions[uid].add(content)

                    url = line["url"]
                    url = url[url.find("www.zhihu.com/question/") + 23:]
                    if "/" in url:
                        url = url[:url.find("/")]
                    url_id = url

                    # if url_id in url_questions:
                    url_questions[url_id].add(content)

            except Exception as e:
                failed_file.append(thisdir)
                print(e)
        print("failed_file:", failed_file)
    id_set = set(x for k, v in questions.items() for x in v)
    urlid_set = set(x for k, v in url_questions.items() for x in v)

    print(len(id_set), "id_set")
    print(len(urlid_set), "urlid_set")
    print(len(id_set & urlid_set), "overlap")
    outdata = {"id_set": questions, "urlid_set": url_questions}
    save_json(outdata, outpath)
    print("over")


def debug_key(rootdirpath, outpath):
    #
    sta_dict = collections.defaultdict(int)

    # type dialog
    types = [x for x in os.listdir(rootdirpath) if not x.endswith("tar.gz")]
    failed_file = []
    for data_type in types:
        #
        if "comment" not in data_type:
            continue

        filedirs = [os.path.join(rootdirpath, data_type)]
        # go down to the dir
        while not [x for x in os.listdir(filedirs[0]) if ".gz" in x]:
            filedirs = [os.path.join(subdir, x)
                        for subdir in filedirs
                        for x in os.listdir(subdir)
                        if os.path.isdir(os.path.join(subdir, x))]

        for thisdir in tqdm.tqdm(filedirs):
            path = os.path.join(thisdir, "zhihu")
            try:
                if os.path.exists(path):
                    data = load_jsonl(path)
                elif os.path.exists(path + ".gz"):
                    data = load_gz_jsonl(path + ".gz")
                else:
                    print("wrong data type", thisdir)
                    continue

                for line in data:
                    if "content" not in line:
                        continue

                    content = line["content"]
                    if "content_type" in line:
                        sta_dict[line["content_type"]] += 1


            except Exception as e:
                failed_file.append(thisdir)
                print(e)
        print("failed_file:", failed_file)

    save_json(sta_dict, outpath)
    print("over")


if __name__ == '__main__':
    # debug_qid("/extension/wangyida/data/dialog/zh/tripartite/aminer/yyq_scp/sta/check_zhihu_id.json",
    #           "/extension/wangyida/data/dialog/zh/tripartite/aminer/yyq_scp/sta/check_zhihu_urlid.json",
    #           "/extension/wangyida/data/dialog/zh/tripartite/aminer/yyq_scp/zhihu/",
    #           "/extension/wangyida/data/dialog/zh/tripartite/aminer/yyq_scp/sta/question.json")
    debug_key("/extension/wangyida/data/dialog/zh/tripartite/aminer/yyq_scp/zhihu/",
              "/extension/wangyida/data/dialog/zh/tripartite/aminer/yyq_scp/sta/debug_key.json")
