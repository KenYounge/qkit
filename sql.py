""" Utilities to support SQL """

import os
import pymysql
import time
import random


MYSQL_DB               = 'mydb'               # Name of the MySQL database
MYSQL_IP               = '###.###.###.###'    # Static IP Assigned in DEV panel
MYSQL_PORT             = 3306
MYSQL_USR              = 'USERNAME'
MYSQL_PWD              = 'USERPASSWORD'
MYSQL_INSTANCE_NAME    = "GCPPROJECTNAME:SQLINSTANCENAME"
MYSQL_RETRIES          = 3


def sql_escape(s):
    return pymysql.escape_string(s)

def sql_cnn():
    print('MySQL.Connection')
    for retries in range(MYSQL_RETRIES + 1):
        if retries > 0:
            print("retry #{}".format(retries))
            time.sleep((2 ** retries) + (random.randint(0, 1000) / 1000))
        try:
            if os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/'):
                db = pymysql.connect(unix_socket='/cloudsql/' + MYSQL_INSTANCE_NAME, db=MYSQL_DB, user=MYSQL_USR, passwd=MYSQL_PWD, charset='utf8')
            else:
                db = pymysql.connect(host=MYSQL_IP, port=MYSQL_PORT, db=MYSQL_DB, user=MYSQL_USR, passwd=MYSQL_PWD, charset='utf8')

            return db
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            print('MySQL.Connection.Error:' + str(e))

def sql_cur(cnn=None):
    if not cnn:
        cnn = sql_cnn()
    cur = cnn.cursor()
    return cnn, cur

def sql_insert(tablename, data, cnn=None, replace=False):
    print('MySQL.Insert: table=' + tablename + ' data=' + str(data))
    try:
        assert tablename
        assert data
        assert data.keys()

        cnn, cur = sql_cur(cnn)
        fields = """`""" + "`, `".join(data.keys()) + """`"""
        params = """%s, """ * (len(data.keys()) - 1) + """%s"""
        values = [data[key] for key in data.keys()]

        sql = "REPLACE" if replace else "INSERT"
        sql += ' INTO ' + tablename + ' (' + fields + ') VALUES (' + params + ')'
        cur.execute(sql, values)
        cnn.commit()

    except Exception as e:
        print('DB INSERT ERROR: ' + str(e))
        print('SQL INSERT: table=' + tablename + ' data=' + str(data))
        return False
    else:
        return True

def sql_fetchall(sql, cnn=None, cur=None):
    print('MySQL.FetchAll: ' + sql)
    if not cur:
        cnn, cur = sql_cur(cnn)
    cur.execute(sql)
    return cur.fetchall()

