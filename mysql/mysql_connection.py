# -*- coding:utf-8 -*-
"""
    mysql
"""
import mysql

# 后台部分账号库
CATCH_SQL_PAS = "Zgamecn6"
# 服务器列表数据库
SERVER_LST_HOST = "5550a4e4a844d.sh.cdb.myqcloud.com:6280"
# FL
CATCH_SQL_HOST = "5591fa7bbdf6e.sh.cdb.myqcloud.com:5804"
# 服务器列表数据库  10.66.104.102:3306
# CATCH_SQL_HOST = "10.66.140.121:3306"
SERVER_GAME_MANAGER_HOST = "10.66.105.83:3306"


def get_log_mysql_connection():
    """
        获取日志数据库连接
    """
    mysql_connect = mysql.Connection(CATCH_SQL_HOST, 'manager', 'root', CATCH_SQL_PAS)
    return mysql_connect


def get_log_mysql_connection_haima():
    """
        获取日志数据库连接
    """
    mysql_connect = mysql.Connection(CATCH_SQL_HOST, 'manager_haima', 'root', CATCH_SQL_PAS)
    return mysql_connect


def get_server_lst_connection():
    """
        获取服务器连接
    """
    mysql_connect = mysql.Connection(SERVER_LST_HOST, 'zgame', 'root', CATCH_SQL_PAS)
    return mysql_connect

def get_game_manager_mysql_connection():
    """
        获取服务器连接
    """
    mysql_connect = mysql.Connection(SERVER_GAME_MANAGER_HOST, 'zgame', 'root', CATCH_SQL_PAS)
    return mysql_connect