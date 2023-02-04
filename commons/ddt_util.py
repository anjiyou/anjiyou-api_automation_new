"""
@File_name:    commons/ddt_util
@Author:         liuwei
@Time:            2023/2/2 13:22
"""
import json

import yaml


def ddt(case_info):
    new_str_case_info_list = []
    parametrize_value_list = case_info[0].get("parametrize")
    name_length = len(parametrize_value_list[0])
    name_list = parametrize_value_list[0]
    need_replace_list = parametrize_value_list[1:len(parametrize_value_list)]
    for i in range(len(parametrize_value_list) - 1):
        if len(need_replace_list[i]) == name_length:
            str_case_info = json.dumps(case_info[0])
            for j in range(len(need_replace_list[i])):
                old_str = name_list[j]
                new_str = str(need_replace_list[i][j])
                str_case_info = str_case_info.replace(f"${old_str}", new_str)
            new_str_case_info_list.append(str_case_info)
        else:
            raise Exception(f"用例输入参数个数有误，请检查！")
    case_info = [json.loads(x) for x in new_str_case_info_list]
    return case_info


def read_testcases(path):
    with open(path, mode="r", encoding="utf-8") as f:
        case_info = yaml.load(stream=f, Loader=yaml.FullLoader)
        if len(case_info) >= 2:
            return [case_info]
        else:
            if "parametrize" in case_info[0].keys():
                case_info = ddt(case_info)
                return case_info
            else:
                return case_info
