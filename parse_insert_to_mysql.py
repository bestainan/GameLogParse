# -*- coding:utf-8 -*-

"""
    抓取日志
    要伴随服务器开启而开启
"""
import os
import sys
import time
import pickle
import datetime
import urllib2
from util import game_define
from mysql import mysql
from util import logs_out_in_path

from action.parse_action import log_parse
from util.logs_out_path_of_parse import *

# 飞流mysql 飞流日志服务器地址
CATCH_SQL_HOST = "5591fa7bbdf6e.sh.cdb.myqcloud.com:5804"

CATCH_SQL_PAS = "Zgamecn6"
#拆分文件目录
LOG_PATH_NAME = CATCH_TODAY_LOGS_DAT_LST
#TODO 该目录要修改路径
CATCH_LOGS_DAT = "/opt/GameLogParse/dat/save_%s.dat"

LOGIN_RECHARGE_LST = ['EVENT_ACTION_ROLE_LOGIN', 'EVENT_ACTION_RECHARGE_PLAYER']

class CatchData(object):
    # 抓取间隔时间
    catch_dis_time = 300
    #最后抓取日期
    last_catch_logs_date = None
    # 抓取行数
    last_catch_logs_line_num = 0
    # mysql 队列
    mysql_queue = []

    def reset(self, server_id):
        """
            重置
        """
        print 'init'
        out_put_file = open(CATCH_LOGS_DAT % str(server_id), 'w')
        dat_dict = dict()
        dat_dict['last_catch_logs_date'] = None
        dat_dict['last_catch_logs_line_num'] = 0
        pickle.dump(dat_dict, out_put_file)
        out_put_file.close()

    def put(self, server_id):
        """
            保存配置
        """
        print 'put'
        out_put_file = open(CATCH_LOGS_DAT % str(server_id), 'w')
        print out_put_file
        dat_dict = dict()
        dat_dict['last_catch_logs_date'] = self.last_catch_logs_date
        dat_dict['last_catch_logs_line_num'] = self.last_catch_logs_line_num
        pickle.dump(dat_dict, out_put_file)
        out_put_file.close()

    def load(self, server_id):
        """
            加载
        """
        print 'load'
        if os.path.exists(CATCH_LOGS_DAT % str(server_id)):
            out_put_file = open(CATCH_LOGS_DAT % str(server_id), 'r')
            dat_dict = pickle.load(out_put_file)
            print "dat_dict:"
            print dat_dict
            self.last_catch_logs_date = dat_dict['last_catch_logs_date']
            self.last_catch_logs_line_num = dat_dict['last_catch_logs_line_num']
            out_put_file.close()


# 开启新进程执行
def start_catch_logs(args):
    print '\n'
    arg_date = datetime.date.today()
    err = open(LOG_PATH+"%s/%s" % ("Error", arg_date)+'_mysql', 'a')
    nor = open(LOG_PATH+"%s/%s" % ("Normal", arg_date)+'_mysql', 'a')
    sys.stdout = nor
    if len(args) > 1:
        try:
            split_date_str = args[1]
            arg_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
            err = open(LOG_PATH+"%s/%s" % ("Error", arg_date)+'_mysql', 'a')
            nor = open(LOG_PATH+"%s/%s" % ("Normal", arg_date)+'_mysql', 'a')
            sys.stdout = nor
            print "arg_date:"
            print arg_date
        except:
            sys.stdout = err
            sys.stderr.write("Err: Use daily_catch_split_log %Y-%m-%d")
            sys.exit(1)
    sys.stdout = nor
    print '\n'

    for _server_id in LOG_PATH_NAME.keys():
        sys.stdout = nor
        catch_data.load(_server_id)
        #计算起始日期
        if not catch_data.last_catch_logs_date:
            catch_data.last_catch_logs_date = arg_date
        print("抓取日期 %s 日志" % catch_data.last_catch_logs_date)
        url_path = LOG_PATH_NAME[_server_id].format(cur_date=catch_data.last_catch_logs_date)
        url = urllib2.urlopen(url_path)
        if url.msg == 'OK':
            log_lines = url.readlines()
            total_lines = len(log_lines)
            # 解析获取日志并添加
            print("catch_data.last_catch_logs_line_num " + str(catch_data.last_catch_logs_line_num))
            print("total_lines " + str(total_lines))
            log_lines = log_lines[catch_data.last_catch_logs_line_num: total_lines]
            print("parse_lines " + str(len(log_lines)))
            parse_game_log(log_lines)
            start_insert_to_mysql()

            #如果不是今天 说明日志已经结束下次加载第二天
            if catch_data.last_catch_logs_date != datetime.date.today():
                catch_data.last_catch_logs_date += datetime.timedelta(days=1)
                catch_data.last_catch_logs_line_num = 0
                print("not today")
                # 清空数据库当天与日志有关的表
                # truncate_mysql_table()
            else:
                # 是今天就记录已经加载的行数 下次增量更新
                catch_data.last_catch_logs_line_num = total_lines
                print("is today")
            # 保存抓取状态信息
            catch_data.put(_server_id)
            catch_data.load(_server_id)
    # time.sleep(300)


def truncate_mysql_table():
    mysql_connect = mysql.Connection(CATCH_SQL_HOST, 'manager_haima', 'root', CATCH_SQL_PAS)
    sql_recharge = "truncate EVENT_ACTION_RECHARGE_PLAYER;"
    sql_login = "truncate EVENT_ACTION_ROLE_LOGIN;"
    mysql_connect.execute(sql_recharge)
    mysql_connect.execute(sql_login)


def parse_game_log(log_lines):
    """
        解析
    """
    # print("准备解析插入日志 数量" + str(len(log_lines)))
    for _log in log_lines:
        _log = _log.strip()
        log_instance = log_parse(_log)
        if not log_instance:
            continue
        _insert_log_to_mysql(log_instance)


def _insert_log_to_mysql(log_dict):
    """
        插入数据到MYSQL队列
    """
    keys = log_dict.keys()
    # print("单条日志所有key：" + str(keys))
    if 'action' not in keys:
        return
    log_action = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(log_dict['action'], 'Err')
    if log_action not in LOGIN_RECHARGE_LST:
        return
    if log_action == 'Err':
        return
    # print("日志事件 " + str(log_action))
    # 插入mysql

    # 插入数据
    str_key_lst = []
    str_val_lst = []
    for key, val in log_dict.items():
        if key == 'team_list':
            continue
        else:
            str_key_lst.append(key)
            if isinstance(val, str) or isinstance(val, datetime.datetime) or isinstance(val, datetime.date):
                str_val_lst.append("'" + str(val) + "'")
            else:
                str_val_lst.append(val)

    str_key_lst = map(str, str_key_lst)
    str_val_lst = map(str, str_val_lst)
    str_key = ','.join(str_key_lst)
    str_val = ','.join(str_val_lst)
    sql = "INSERT INTO %s (%s) VALUES (%s);" % (log_action, str_key, str_val)
    catch_data.mysql_queue.append(sql)


def start_insert_to_mysql():
    """
        插入mysql
    """
    mysql_connect = mysql.Connection(CATCH_SQL_HOST, 'manager_haima', 'root', CATCH_SQL_PAS)

    sleep_time = float(1) / float(500)

    while len(catch_data.mysql_queue):
        queue_num = len(catch_data.mysql_queue)
        # print("准备插入mysql当前队列长度 " + str(queue_num))
        _sql = ''
        for i in xrange(min(queue_num, 5000)):
            _sql += catch_data.mysql_queue.pop()
        # print("_sql " + str(_sql) + "|")
        if _sql:
            mysql_connect.execute(_sql)
        time.sleep(sleep_time)

# def start():
#     try:
#         _threads = [
#             threading.Thread(target=_start_catch_logs),
#             # threading.Thread(target=start_insert_to_mysql),
#         ]
#
#         for _th in _threads:
#             _th.start()
#
#         for _th in _threads:
#             _th.join()
#
#     except Exception, e:
#         print(e)
#     print("all thread is done!")
# start_catch_logs(['2015-06-15'])


def reset_catch_data():
    for _server_id in LOG_PATH_NAME.keys():
        catch_data.reset(_server_id)
        catch_data.load(_server_id)


catch_data = CatchData()
# reset_catch_data()
#
if __name__ == '__main__':
    start_time = datetime.datetime.now()
    print start_time
    start_catch_logs(sys.argv)
    end_time = datetime.datetime.now()
    print end_time
    print end_time-start_time

