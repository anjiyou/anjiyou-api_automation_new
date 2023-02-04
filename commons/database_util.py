"""
@File_name:    commons/database_util
@Author:         liuwei
@Time:            2023/2/2 11:15
"""
import pymysql


class DatabaseUtil(object):
    def db_connect(self):
        connect = pymysql.connect(
            user="root",
            password="liuwei.520",
            host="localhost",
            database="phpwind",
            port=3306,
        )
        return connect

    def search_result(self,sql):
        connect = self.db_connect()
        cursor = connect.cursor()
        cursor.execute(sql)
        value = cursor.fetchall()
        cursor.close()
        connect.close()
        return value


if __name__ == '__main__':
    db = DatabaseUtil()
    sql = "select name from user"
    value = db.search_result(sql)
    print(value)
