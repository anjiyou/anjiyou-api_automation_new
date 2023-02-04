"""
@File_name:    commons/yaml_util
@Author:         liuwei
@Time:            2023/1/31 12:28
"""
import yaml


def read_yaml(path):
    with open(path,mode="r",encoding="utf-8") as f:
        result = yaml.load(stream=f,Loader=yaml.FullLoader)
        return result


def write_yaml(path,data):
    with open(path,mode="a",encoding="utf-8") as f:
        yaml.dump(data,stream=f,allow_unicode=True)


def clear_yaml(path):
    with open(path,mode="w",encoding="utf-8") as f:
        f.truncate()


