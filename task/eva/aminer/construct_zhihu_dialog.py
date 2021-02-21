import os
import tqdm
import pdb
import gc
import collections

from data_utils import *


def zhihu_format(rootdirpath, outpath, id_type="urlid"):
    #
    data_dict = {}
    multi_question = 0

    # type dialog
    types = [x for x in os.listdir(rootdirpath) if not x.endswith("tar.gz")]
    failed_file = []
    for data_type in types:
        if not os.path.isdir(os.path.join(rootdirpath, data_type)):
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
                    if "content" not in line or len(line["content"]) == 0:
                        continue
                    content = line["content"]

                    if id_type == "urlid":
                        url = line["url"]
                        url = url[url.find("www.zhihu.com/question/") + 23:]
                        if "/" in url:
                            url = url[:url.find("/")]
                        id = url
                    elif id_type == "pid":
                        if "qid" not in line and "pid_str" not in line:
                            continue
                        if "qid" in line and "pid_str" in line and str(line["qid"]) != str(line["pid_str"]):
                            continue
                        id_k = "qid" if "qid" in line else "pid_str"
                        id = str(line[id_k])

                    else:
                        raise Exception

                    idstr = "" if "idstr" not in line else line["idstr"]

                    if id not in data_dict:
                        data_dict[id] = {"questions": collections.defaultdict(list),
                                         "comments": collections.defaultdict(list),
                                         "answers": collections.defaultdict(list)}

                    if data_type == "qa":
                        data_dict[id]["questions"][idstr].append(content)
                    elif data_type == "answer":
                        data_dict[id]["answers"][idstr].append(content)
                    else:
                        data_dict[id]["comments"][idstr].append(content)

            except Exception as e:
                failed_file.append(thisdir)
                print(e)
        print("failed_file:", failed_file)
    data_dict = {k: v for k, v in data_dict.items() if
                 len(v["questions"]) > 0 and (len(v["comments"]) > 0 or len(v["answers"]) > 0)}
    print(sum(len(v["answers"]) for k, v in data_dict.items()), "answers")
    print(sum(len(v["comments"]) for k, v in data_dict.items()), "comments")
    print(len(data_dict), "questions")

    save_json(data_dict, outpath)
    del data_dict
    gc.collect()

    print("zhihu data format over")
    return


def extract_jsonl(path, outdir, batch_size=500000):
    data = load_json(path)
    outdata = set()
    while len(data):
        v = data.popitem()
        for context in v["question"]:
            for qa in v["answers"]:
                dialog = "<\t>".join([context, qa])
                outdata.add(dialog)

    outdata = list(outdata)
    i = 0
    while i + batch_size < len(outdata):
        outpath = os.path.join(outdir, "zhihu{}".format(i))
        save_jsonl(outdata[i: i+batch_size], outpath)
        i += batch_size
    if i < len(outdata):
        outpath = os.path.join(outdir, "zhihu{}".format(i))
        save_jsonl(outdata[i:], outpath)
    del outdata
    gc.collect()
    #             if len(outdata) == batch_size:
    #                 outdata = [x.split("<\t>") for x in outdata]
    #                 outpath = os.path.join(outdir, "zhihu{}".format(fid))
    #                 save_jsonl(outdata, outpath)
    #                 fid += len(outdata)
    #                 outdata = set()
    # if len(outdata) > 0:
    #     outdata = [x.split("<\t>") for x in outdata]
    #     outpath = os.path.join(outdir, "zhihu{}".format(fid))
    #     save_jsonl(outdata, outpath)
    return


if __name__ == '__main__':
    # "/extension/wangyida/data/dialog/zh/tripartite/aminer/yyq_scp/zhihu/"
    zhihu_format("/extension/wangyida/data/dialog/zh/tripartite/aminer/yyq_scp/zhihu/",
                 "/extension/wangyida/data/dialog/zh/tripartite/aminer/yyq_scp/zhihu/zhihu_pid.json",
                 id_type="pid")
    # zhihu_format("/home/wangyida/git/data/dialog/zh/aminer/zhihu/",
    #              "/home/wangyida/git/data/dialog/zh/aminer/zhihu/zhihu_pid.json",
    #              id_type="pid")
    # zhihu_format("/home/wangyida/git/data/dialog/zh/aminer/zhihu/",
    #              "/home/wangyida/git/data/dialog/zh/aminer/zhihu/zhihu_urlid.json",
    #              id_type="urlid")
