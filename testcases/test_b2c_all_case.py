"""
@File_name:    testcases/a_user/test_b2c
@Author:         liuwei
@Time:            2023/2/2 19:43
"""
from pathlib import Path
import allure
import pytest
from commons import yaml_util
from commons.ddt_util import read_testcases
from commons.request_util import RequestUtil


@allure.epic("项目名称：码尚教育B2C商城自动化接口测试")
class TestB2c(object):
    pass


current_path = Path(__file__).parent
yaml_path_list = current_path.glob("**/*.yaml")


# 创建测试用例
def create_testcase(yaml_path):
    case_info_list = yaml_util.read_yaml(yaml_path)
    case_feature = case_info_list[0]["feature"]
    case_story = case_info_list[0]["story"]
    if len(case_info_list) > 1:
        case_story = case_feature

    @allure.feature(case_feature)
    @allure.story(case_story)
    @pytest.mark.parametrize("case_info", read_testcases(yaml_path))
    def test_func(self, case_info, base_url):
        if isinstance(case_info, list):
            for case in case_info:
                allure.dynamic.title(case["title"])
                RequestUtil().standard_yaml(case, base_url)
        else:
            allure.dynamic.title(case_info["title"])
            RequestUtil().standard_yaml(case_info, base_url)
    return test_func


for yaml_path in yaml_path_list:
    yaml_name = yaml_path.name[:-5]
    func = create_testcase(yaml_path)
    setattr(TestB2c, yaml_name, func)
