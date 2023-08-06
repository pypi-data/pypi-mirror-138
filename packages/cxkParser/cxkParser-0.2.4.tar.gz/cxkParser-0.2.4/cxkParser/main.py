import argparse
import pandas as pd
import os
import requests
import math
import threading
from bs4 import BeautifulSoup
from uuid import uuid4

base_url = "https://marinegenomics.oist.jp/habu/genesearch/genemodel?utf8=%E2%9C%93&gene_modelid="
url_suffix = "&project_id=1"

result_list = []
file_name_list = []


def not_empty(str):
    return str and str.strip()


def is_file(path):
    return os.path.isfile(path)


@DeprecationWarning
def gen_token():
    return uuid4().hex[:8]


def read_data(path):
    model_list = []
    for file in os.listdir(path):
        if is_file(os.path.join(path, file)):
            print(file)
            file_name_list.append(str(file))
        file_suffix = file.split('.')[-1]
        if file_suffix not in ['csv', 'xlsx', 'xls']:
            continue
        full_path = os.path.join(path, file)
        if file_suffix == 'csv':
            data = pd.read_csv(full_path)
        else:
            data = pd.read_excel(full_path)
        if 'target_id' not in data:
            raise Exception("请调好格式，以target_id作为那个id的列名")
        model_list.append(data['target_id'])
    return model_list


def model_split(model_list, thread_num):
    concurrency_model_list = []
    for model in model_list:
        num_per_group = math.ceil(len(model) / thread_num)
        concurrency_model_list.append(
            [model[i:i+num_per_group] for i in range(0, len(model), num_per_group)])
    return concurrency_model_list


def parse_concurrency(model_group):
    for id in model_group:
        full_url = base_url + id + url_suffix
        doc = requests.get(full_url).text
        doc = BeautifulSoup(doc, features="lxml")
        flag = doc.find(
            "div", id="pfam-domain-list")
        if flag is None:
            result_list.append({"target_id": str(id), "annotation": None})
        else:
            annotation = flag.get_text().strip().splitlines()
            annotation = list(filter(not_empty, annotation))
            result_list.append(
                {"target_id": str(id), "annotation": annotation[3]})
        print(f"{id}: done")


def save(output_path, result_list, file_name):
    df = pd.DataFrame.from_dict(result_list)
    df.index += 1
    if is_file(output_path):
        df.to_excel(output_path)
    else:
        output_path = os.path.join(output_path, 'annotation_' + file_name)
        df.to_excel(output_path)


class cxkTask(threading.Thread):
    def __init__(self, threadID, name, task):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.task = task

    def run(self):
        parse_concurrency(self.task)
        print(f"{self.name} 线程退出")


def main():
    parse_args = argparse.ArgumentParser()
    parse_args.add_argument('--path', '-p', default=None,
                            required=True, type=str, help="请输入文件根目录")
    parse_args.add_argument('--output', '-o', default=None,
                            required=True, type=str, help="请输入文件的输出目录和文件名, 若不输入文件名，将自动生成8位的token作为文件名")
    parse_args.add_argument('--thread_nums', '-n',
                            default=1, required=False, type=int, help="请输入线程数量，默认不开启")
    args = parse_args.parse_args()

    model_list = read_data(args.path)
    model_list_group = model_split(model_list, args.thread_nums)
    thread_list = []
    for i in range(len(model_list)):
        for j in range(args.thread_nums):
            thread = cxkTask(j, "Thread-" + str(j),
                             model_list_group[i][j])
            thread_list.append(thread)
        for t in thread_list:
            t.start()
        for t in thread_list:
            t.join()
        save(args.output, result_list, file_name_list[i])
        thread_list.clear()
        result_list.clear()


if __name__ == '__main__':
    main()
