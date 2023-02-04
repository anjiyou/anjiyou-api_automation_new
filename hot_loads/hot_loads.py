"""
@File_name:    hot_loads/hot_loads
@Author:         liuwei
@Time:            2023/1/31 20:31
"""
import base64
import hashlib
import os
import random
import re
import time
from pathlib import Path
import rsa
import yaml

current_path = str(Path(__file__).parent)


class DebugTalk(object):
    def read_yaml(self, path=current_path + "./../extract.yaml", key=None):
        with open(path, mode="r", encoding="utf-8") as f:
            result = yaml.load(stream=f, Loader=yaml.FullLoader)
            return result[key]

    def get_random_num(self, length):
        num_str = str(int(time.time()))
        return num_str[:length]

    def md5_encode(self, key=None):
        str_key = str(key).encode("utf-8")
        md5_value = hashlib.md5(str_key).hexdigest()
        return md5_value

    def base64_encode(self, key):
        str_key = str(key).encode("utf-8")
        base64_value = base64.b64encode(str_key).decode(encoding="utf-8")
        return base64_value

    def create_key(self):
        (public_key, private_key) = rsa.newkeys(1024)
        f = open("./public.pem", mode="wt", encoding="utf-8")
        f.write(public_key.save_pkcs1().decode())
        f.close()
        f = open("./private.pem", mode="wt")
        f.write(private_key.save_pkcs1().decode())
        f.close()

    def rsa_encode(self, key):
        path = os.getcwd()
        f = open(f"{path}/hot_loads/public.pem", mode="r", encoding="utf-8")
        public_key = rsa.PublicKey.load_pkcs1(f.read().encode())
        f.close()
        # 把字符串转化成utf-8格式
        key = str(key).encode("utf-8")
        # 把字符串加密成byte类型
        byte_value = rsa.encrypt(key, public_key)
        # 把字节转化成字符串类型
        rsa_value = base64.b64encode(byte_value).decode("utf-8")
        return rsa_value

    def sign(self, key=None):
        with open(key, mode="r", encoding="utf-8") as f:
            case_info_list = yaml.load(f, Loader=yaml.FullLoader)
        for case_info in case_info_list:
            temp_dict = {}
            case_info_request = case_info["request"]
            url = str(case_info_request["url"])
            url_pattern_list = url[url.index("?") + 1::].split("&")
            for value in url_pattern_list:
                temp_dict[value.split("=")[0]] = value.split("=")[1]
            if "params" in case_info_request.keys():
                params_dict = case_info_request["params"]
                temp_dict.update(params_dict)
            if "data" in case_info_request.keys():
                data_dict = case_info_request["data"]
                temp_dict.update(data_dict)
            # 第一步：先将url和params、data里的参数按照ascii码升序，然后格式key=value使用&拼接在一起
            temp_dict = dict(sorted(temp_dict.items(), key=lambda x: x[0]))
            str_sign = ""
            for key,value in temp_dict.items():
                str_sign += f"{key}={value}&"
            str_sign = str_sign[:len(str_sign)-1:]
            # 第二歩：把appid、appseceret拼接在头部
            appid = "liuwei"
            appsecret = "liuwei.520"
            str_sign = f"appid={appid}&appsecret={appsecret}&{str_sign}"
            # 第三歩：把订单号和时间戳拼接到尾部
            order_num = random.randint(1000,9999)
            time_stamp = str(time.time())
            str_sign = f"{str_sign}&order_num={order_num}&time_stamp={time_stamp}"
            # 第四歩：进行32位MD5加密
            str_sign = self.md5_encode(str_sign)
            return str_sign






if __name__ == '__main__':
    print(DebugTalk().rsa_encode("admin"))
