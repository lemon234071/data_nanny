| dataset | size | sessions | sents | avg turn | max turn | min turn |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `好大夫中文医疗问答数据` | 2.51 GB | 1040709 | 6645229 | 1.89 | 253 | 1 |
| `京东客服对话数据` | 2.29 GB | 1023843 | 20450436 | 6.36 | 37 | 1 |
| `京东多模态客服对话数据` | 508.62 MB | 221487 | 4969780 | 6.99 | 149 | 1 |
| `买车网问答数据` | 202.19 MB | 668317 | 1336634 | 1 | 1 | 1 |
| `中文医疗对话数据集` | 372.0 MB | 792099 | 1584198 | 1 | 1 | 1 |
| `CMedQA2` | 89.45 MB | 226266 | 346266 | 1 | 1 | 1 |


# info
1. 好大夫中文医疗问答数据
    * `/home/data/tripartite/zhiyuan/强语义数据/中文医疗问答数据-好大夫/中文医疗问答数据-好大夫`
```bash
python mds.py /home/data/tripartite/zhiyuan/强语义数据/中文医疗问答数据-好大夫/中文医疗问答数据-好大夫
```

2. 京东客服对话数据
    * `/home/data/tripartite/zhiyuan/强语义数据/京东对话2019数据集`
```bash
python jdqa19.py /home/data/tripartite/zhiyuan/强语义数据/京东对话2019数据集/JDDC_Dataset_LREC.txt
```

3. 京东多模态客服对话数据
    * `/home/data/tripartite/zhiyuan/强语义数据/京东对话2020`
```bash
python jdqa20.py /home/data/tripartite/zhiyuan/强语义数据/京东对话2020
```

4. 买车网问答数据
    * `/home/data/tripartite/zhiyuan/强语义数据/买车网问答数据集/QA_maichewang_data.json`
    
5. 中文医疗对话数据集
    * `/home/data/tripartite/zhiyuan/强语义数据/6个科室的问答数据`
```bash
python cmdd.py /home/data/tripartite/zhiyuan/强语义数据/6个科室的问答数据/Data_数据
```

6. CMedQA2
    * `/home/data/tripartite/zhiyuan/强语义数据/medqa/cMedQA2`
```bash
python medqa.py \
/home/data/tripartite/zhiyuan/强语义数据/medqa/cMedQA2/answer.csv \
/home/data/tripartite/zhiyuan/强语义数据/medqa/cMedQA2/question.csv
```
