"""
@File_name:    commons/global_args
@Author:         liuwei
@Time:            2023/2/2 18:27
"""
from pathlib import Path

from iniconfig import IniConfig


def load_ini():
    path = Path("./pytest.ini")
    if not path.exists():
        return {}
    else:
        ini = IniConfig("./pytest.ini")
        if "apitest" not in ini:
            return {}
        else:
            return dict(ini["apitest"].items())


if __name__ == '__main__':
    print(load_ini())
