"""
@File_name:    commons/assert_util
@Author:         liuwei
@Time:            2023/2/1 22:35
"""
import logging

import jsonpath

from commons.database_util import DatabaseUtil
logger = logging.getLogger(__name__)


def assert_code(expect_value, real_value):
    if int(expect_value) != real_value:
        raise_assert_error(f"code 断言失败,预期结果:{expect_value},实际结果:{real_value}")


def assert_equals(expect_value, real_value):
    for key,value in expect_value.items():
        real_value = jsonpath.jsonpath(real_value.json(),f"$..{key}")
        try:
            if value not in real_value:
                raise_assert_error(f"equals 断言失败,预期结果:{value},实际结果:{real_value}")
                logger.info("结果：测试用例失败")
        except:
            raise_assert_error(f"equals 断言失败,预期结果:{value},实际结果:{real_value}")


def assert_contains(expect_value, real_value):
    if expect_value not in real_value:
        raise_assert_error(f"contains 断言失败,预期结果:{expect_value},实际结果:{real_value}")


def raise_assert_error(msg):
    logger.error(msg)
    logger.info("结果：测试用例失败")
    logger.info("-----------------------测试用例请求结束-----------------------\n")
    raise AssertionError(msg)


def assert_database(expect_value):
    for key,value in expect_value.items():
        real_value = DatabaseUtil().search_result(value)
        if key == real_value[0]:
            raise_assert_error(f"database 断言失败,预期结果:{key},实际结果:{real_value}")


def assert_result(validate_key, expect_value, response):
    if validate_key == "code":
        assert_code(expect_value, response.status_code)
    elif validate_key == "equals":
        assert_equals(expect_value, response)
    elif validate_key == "contains":
        assert_contains(expect_value, response.text)
    elif validate_key == "database":
        assert_database(expect_value)
    else:
        print("不支持的断言！")
