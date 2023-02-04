"""
@File_name:    commons/request_util
@Author:         liuwei
@Time:            2023/1/31 12:32
"""
import json
import logging
import re
from pathlib import Path

import jsonpath
import yaml
from requests import sessions

from commons import yaml_util, global_args
from commons.assert_util import assert_result
from hot_loads.hot_loads import DebugTalk

current_path = str(Path(__file__).parent)
logger = logging.getLogger(__name__)


class RequestUtil(object):
    session = sessions.Session()

    def standard_yaml(self, case_info: dict,base_url=None):
        logger.info("-----------------------测试用例请求开始-----------------------")
        case_info = self.replace_yaml(case_info)
        case_keys = case_info.keys()
        if set(case_keys).issuperset({"feature","title", "request", "validate"}):
            logger.info(f"用例标题：{case_info['title']}")
            case_info_request = case_info["request"]
            if set(case_info_request).issuperset({"method", "url"}):
                method = case_info_request.pop("method")
                logger.info(f"请求方式：{method}")
                if "http" in str(case_info_request):
                    url = case_info_request.pop("url")
                else:
                    url = base_url + case_info_request.pop("url")
                logger.info(f"请求路径：{url}")
                if case_info_request:
                    if set(case_info_request).issuperset({"headers"}):
                        logger.info(f"请求头：{case_info_request['headers']}")
                    # 加入公共参数
                    if set(case_info_request).issuperset({"params"}):
                        params = case_info_request["params"]
                        params.update(global_args.load_ini())
                        case_info_request["params"] = params
                    else:
                        params = {}
                        params.update(global_args.load_ini())
                        case_info_request["params"] = params
                    for key, value in case_info_request.items():
                        if key == "params":
                            logger.info(f"用例params参数：{case_info_request['params']}")
                        elif key == "data":
                            logger.info(f"用例data参数：{case_info_request['data']}")
                        elif key == "json":
                            logger.info(f"用例json参数：{case_info_request['json']}")
                        if key == "files":
                            logger.info(f"用例json参数：{case_info_request['files']}")
                            for file_key, file_value in value.items():
                                value[file_key] = open(file_value, mode="rb")
                    response = self.send_all_request(method, url, **case_info_request)
                    logger.info(f"预期结果：{case_info['validate']}")
                    logger.info(f"实际结果：{response.text}")
                else:
                    response = self.send_all_request(method, url)
                if case_info["validate"]:
                    validate_dict = case_info["validate"]
                    for validate_key, expect_value in validate_dict.items():
                        assert_result(validate_key, expect_value, response)
                logger.info("结果：测试用例通过")
                self.save_extract(case_info, response)
                logger.info("-----------------------测试用例请求结束-----------------------\n")
                return response
            else:
                print("YAML里request目录下必须有method、url")
                logger.info("-----------------------测试用例请求结束-----------------------\n")

        else:
            print("YAML一级目录必须有feature、title、request、validate")
            logger.info("-----------------------测试用例请求结束-----------------------\n")

    def send_all_request(self, method, url, **case_info):
        response = RequestUtil.session.request(method, url, **case_info)
        return response

    def save_extract(self, case_info, response):
        path = current_path + "./../extract.yaml"
        if set(case_info.keys()).issuperset({"extract"}):
            for key, pattern in case_info["extract"].items():
                search_value = re.search(pattern,response.text)
                if search_value:
                    data = {key: search_value[1]}
                    yaml_util.write_yaml(path, data)

    def replace_yaml(self, case_info):
        str_case_info = str(case_info)
        regx = "\\${(.*?)\\((.*?)\\)}"
        hot_load_value_list = re.findall(regx, str_case_info)
        if hot_load_value_list:
            for i in range(len(hot_load_value_list)):
                replace_old = re.search(regx,str_case_info)[0]
                func_str, key = hot_load_value_list[i]
                function = getattr(DebugTalk(), func_str)
                replace_value = function(key=key)
                str_case_info = str_case_info.replace(replace_old, replace_value)
            case_info = yaml.safe_load(str_case_info)
            return case_info
        else:
            return case_info
