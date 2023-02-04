"""
@File_name:    /conftest
@Author:         liuwei
@Time:            2023/1/30 14:48
"""
import os

import pytest

from commons.yaml_util import clear_yaml


@pytest.fixture(scope="session",autouse=True)
def clear_extract_yaml():
    path = os.getcwd() + "/extract.yaml"
    clear_yaml(path)
