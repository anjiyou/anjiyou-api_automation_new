"""
@File_name:    /run
@Author:         liuwei
@Time:            2023/1/30 16:08
"""
import datetime
import os
import time
import pytest

if __name__ == '__main__':
    pytest.main()
    time.sleep(3)
    folder = datetime.datetime.now().strftime("%Y_%d_%m~%H%M%S")
    log_path = os.getcwd() + "/reports/" + folder
    os.mkdir(log_path)
    os.system(f"allure generate ./temps -o {log_path} --clean")