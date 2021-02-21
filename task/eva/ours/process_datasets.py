import os
import json
import collections

ROOTDIR = "/home/wangyida/git/data/dialog/cn/LCCC-plus/"


def save_jsonl(lines, outpath):
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join([json.dumps(line, ensure_ascii=False) for line in lines]))


def from_json(path):
    with open(path, encoding="utf-8") as f:
        lines = json.load(f)
    return lines


def txt_by_emptyline(path):
    dataset = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        dialog = []
        for line in f.readlines():
            line = line.strip()
            if line != "":
                dialog.append(line)
            else:
                dataset.append(dialog)
                dialog = []
    return dataset


def pro_NLPCC2018_task5(path, rootdir):
    outdir = os.path.join(rootdir, "NLPCC2018_task5")
    os.mkdir(outdir)
    # extract data
    dataset = txt_by_emptyline(path)
    print("dataset len:", len(dataset))
    print(dataset[0])
    # save data into jsonl

    save_jsonl(dataset, os.path.join(outdir, "dialog.jsonl"))
    return


def pro_weibo169(dirpath, rootdir):
    for file in os.listdir(dirpath):
        path = os.path.join(dirpath, file)
        outdir = os.path.join(rootdir, file + "_weibo169")
        if os.path.exists(outdir):
            continue
        os.mkdir(outdir)

        dataset = txt_by_emptyline(path)
        print("dataset len:", len(dataset))
        print(dataset[0])

        save_jsonl(dataset, os.path.join(outdir, "dialog.jsonl"))
    return


def pro_weibo0813(dirpath, rootdir):
    files = [x for x in os.listdir(dirpath) if x.endswith(".json")]
    for file in files:
        path = os.path.join(dirpath, file)
        save_dir = os.path.join(rootdir, file + "_weibo0813")
        os.mkdir(save_dir)

        idx = []
        out_dialog = []
        out_persona = []
        out_weibo = []
        cnt_attr = collections.defaultdict(int)
        with open(path, encoding="utf-8") as f:
            for i, line in enumerate(f.readlines()):
                line = json.loads(line)
                cnt_attr["cnt_dialog"] += 1
                idx.append({"weiboid": line["weibo"].get("weiboid", ""), "cids": [seq[0] for seq in line["dialog"]]})
                cnt_attr["weiboid"] += int(line["weibo"].get("weiboid", "") != "")

                out_dialog.append([seq[1].replace(" ", "").replace("\u200b", "") for seq in line["dialog"]])

                new_persona = []
                for uid in line["uids"]:
                    if uid != "NA":
                        persona = line["persona"][uid]
                        new_persona.append(
                            {"gender": persona.get("gender", ""),
                             "location": persona.get("location", "").replace("\u200b", ""),
                             "tags": persona.get("tags", "").replace(" ", "").replace("\u200b", "")})
                        cnt_attr["gender"] += int(persona.get("gender", "") != "")
                        cnt_attr["location"] += int(persona.get("location", "") != "")
                        cnt_attr["tags"] += int(persona.get("tags", "") != "")
                        cnt_attr["cnt_seq"] += 1
                    else:
                        new_persona.append({"gender": "", "location": "", "tags": ""})
                out_persona.append(new_persona)

                out_weibo.append(
                    line["weibo"]["weiboinfo"].get("weibo_cont", "").replace(" ", "").replace("\u200b", ""))
                cnt_attr["weibo_cont"] += int(line["weibo"]["weiboinfo"].get("weibo_cont", "") != "")
        print("len data", len(out_dialog))
        print(cnt_attr)

        print(out_dialog[0])
        save_jsonl(out_dialog, os.path.join(save_dir, "dialog.json"))
        save_jsonl(out_persona, os.path.join(save_dir, "persona.json"))
        save_jsonl(out_weibo, os.path.join(save_dir, "weibo.json"))
        save_jsonl(idx, os.path.join(save_dir, "index.json"))


def pro_others(dirpath, rootdir):
    for file in os.listdir(dirpath):
        if file.startswith("weibo"):
            continue
        outdir = os.path.join(rootdir, file)
        os.mkdir(outdir)

        path = os.path.join(dirpath, file)
        dataset = from_json(path)
        print("dataset len:", len(dataset))
        print(dataset[0])
        save_jsonl(dataset, os.path.join(outdir, "dialog.jsonl"))


def extract_all_dataset():
    """
    Format data as in READEME
    """

    # weibo0813
    pro_weibo0813("/home/wangyida/git/data/dialog/cn/weibo_0813/raw/", ROOTDIR)
    # weibo169
    pro_weibo169("/home/wangyida/git/data/dialog/cn/weibo169/", ROOTDIR)
    # NLPCC2018
    pro_NLPCC2018_task5("/home/wangyida/git/data/dialog/cn/NLPCC2018_task5/train.txt",
                        ROOTDIR)
    # others
    pro_others("/home/wangyida/git/data/dialog/cn/LCCD/other/raw/", ROOTDIR)
    return


if __name__ == '__main__':
    extract_all_dataset()
