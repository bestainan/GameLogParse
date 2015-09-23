# -*- coding:utf-8 -*-

"""
    抓取日志
    要伴随服务器开启而开启
"""
import os
import sys
import time
import pickle
import stat
import datetime
from util import game_define
from mysql import mysql
from action.parse_action import log_parse
from util.logs_out_path_of_parse import *

# 飞流mysql 飞流日志服务器地址
CATCH_SQL_HOST = "5591fa7bbdf6e.sh.cdb.myqcloud.com:5804"

CATCH_SQL_PAS = "Zgamecn6"
# 拆分文件目录

CATCH_LOGS_DAT = "/home/ubuntu/data/HaiMaLogParse/mysql_check/dat/log_save_%s.dat"

LOGIN_RECHARGE_LST = ['EVENT_ACTION_ROLE_LOGIN', 'EVENT_ACTION_RECHARGE_PLAYER']

LOCAL_LOG_PATH_NAME_LST = {
    10003: "/home/ubuntu/data/HaiMaLogs/10003_{cur_date}/10003_{cur_date}_00000",
    10004: "/home/ubuntu/data/HaiMaLogs/10004_{cur_date}/10004_{cur_date}_00000",
    10005: "/home/ubuntu/data/HaiMaLogs/10005_{cur_date}/10005_{cur_date}_00000",
    10006: "/home/ubuntu/data/HaiMaLogs/10006_{cur_date}/10006_{cur_date}_00000",
}
CHECK_PATH = "/home/ubuntu/data/HaiMaLogParse/mysql_check/"


class CatchData(object):
    # 最后抓取日期
    last_catch_logs_date = None
    # 抓取行数
    last_catch_logs_line_num = 0
    # mysql 队列
    mysql_queue = []

    def reset(self, server_id):
        """
            重置
        """
        print '重置'
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
        print '保存配置'
        out_put_file = open(CATCH_LOGS_DAT % str(server_id), 'w')
        dat_dict = dict()
        dat_dict['last_catch_logs_date'] = self.last_catch_logs_date
        dat_dict['last_catch_logs_line_num'] = self.last_catch_logs_line_num
        pickle.dump(dat_dict, out_put_file)
        out_put_file.close()

    def load(self, server_id):
        """
            加载
        """
        print '加载配置:'
        if os.path.exists(CATCH_LOGS_DAT % str(server_id)):
            out_put_file = open(CATCH_LOGS_DAT % str(server_id), 'r')
            dat_dict = pickle.load(out_put_file)
            print "上次插入日期:"+str(dat_dict['last_catch_logs_date']), "上次插入行数位置:"+str(dat_dict['last_catch_logs_line_num'])
            self.last_catch_logs_date = dat_dict['last_catch_logs_date']
            self.last_catch_logs_line_num = dat_dict['last_catch_logs_line_num']
            out_put_file.close()


# 开启新进程执行
def start_catch_logs(args):
    arg_date = datetime.date.today()
    if len(args) > 1:
        try:
            split_date_str = args[1]
            if split_date_str == "reset":
                reset_catch_data()
                return
            if split_date_str == "load":
                server_id = args[2]
                catch_data.load(server_id)
                return
            arg_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
        except:
            sys.stderr.write("Err: Use daily_catch_split_log %Y-%m-%d")
            sys.exit(1)

    for _server_id in LOCAL_LOG_PATH_NAME_LST:
        try:
            start_time = datetime.datetime.now()
            print str(_server_id), '解析开始', start_time
            catch_data.load(_server_id)
            # 计算起始日期
            if not catch_data.last_catch_logs_date:
                catch_data.last_catch_logs_date = arg_date

            # 解析过程记录
            nor = open(CHECK_PATH+"%s/%s" % ("Normal", catch_data.last_catch_logs_date), 'a+')
            sys.stdout = nor

            print("抓取日期 %s 日志" % catch_data.last_catch_logs_date)
            read_file = LOCAL_LOG_PATH_NAME_LST[_server_id].format(cur_date=catch_data.last_catch_logs_date)
            open_file = open(read_file, 'r')
            if open_file:
                log_lines = open_file.readlines()
                total_lines = len(log_lines)
                # 解析获取日志并添加
                print("总行数 " + str(total_lines))
                log_lines = log_lines[catch_data.last_catch_logs_line_num: total_lines]
                print("本次插入行数 " + str(len(log_lines)))
                parse_game_log(log_lines, catch_data.last_catch_logs_date)
                create_table_in_mysql(catch_data.last_catch_logs_date)
                start_insert_to_mysql()

                # 如果不是今天 说明日志已经结束下次加载第二天
                if catch_data.last_catch_logs_date != datetime.date.today():
                    catch_data.last_catch_logs_date += datetime.timedelta(days=1)
                    catch_data.last_catch_logs_line_num = 0
                    print("不是今天")
                    # 清空数据库当天与日志有关的表
                    # truncate_mysql_table()
                else:
                    # 是今天就记录已经加载的行数 下次增量更新
                    catch_data.last_catch_logs_line_num = total_lines
                    print("是今天")
                # 保存抓取状态信息
                catch_data.put(_server_id)
                catch_data.load(_server_id)

                sys.stdout = nor
                end_time = datetime.datetime.now()
                print str(_server_id), '解析结束', end_time
                print '共花费时间', (end_time-start_time).seconds, '秒'
                print "-----------------------------------------"
        except Exception, e:
            err = open(CHECK_PATH+"%s/%s" % ("Error", catch_data.last_catch_logs_date), 'a+')
            sys.stdout = err
            print datetime.datetime.now(), _server_id, catch_data.last_catch_logs_date, "  Error:", e
            print "--------------------"
            pass


def truncate_mysql_table():
    mysql_connect = mysql.Connection(CATCH_SQL_HOST, 'manager_haima', 'root', CATCH_SQL_PAS)
    sql_recharge = "truncate EVENT_ACTION_RECHARGE_PLAYER;"
    sql_login = "truncate EVENT_ACTION_ROLE_LOGIN;"
    mysql_connect.execute(sql_recharge)
    mysql_connect.execute(sql_login)


def parse_game_log(log_lines, arg_date):
    """
        解析
    """
    for _log in log_lines:
        _log = _log.strip()
        log_instance = log_parse(_log)
        if not log_instance:
            continue
        _insert_log_to_mysql(log_instance, arg_date)


def _insert_log_to_mysql(log_dict, arg_date):
    """
        插入数据到MYSQL队列
    """
    keys = log_dict.keys()
    if 'action' not in keys:
        return
    log_action = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(log_dict['action'], 'Err')
    if log_action not in LOGIN_RECHARGE_LST:
        return
    if log_action == 'Err':
        return

    # 插入数据
    str_key_lst = []
    str_val_lst = []
    for key, val in log_dict.items():
        if key == 'team_list':
            continue
        if key == 'player_name':
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
    sql = "INSERT INTO %s (%s) VALUES (%s);" % (log_action + '_' + arg_date.strftime("%Y%m%d"), str_key, str_val)
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


def create_table_in_mysql(arg_date):
    mysql_connect = mysql.Connection(CATCH_SQL_HOST, 'manager_haima', 'root', CATCH_SQL_PAS)

    role_login_str = "EVENT_ACTION_ROLE_LOGIN_" + arg_date.strftime("%Y%m%d")
    recharge_player_str = "EVENT_ACTION_RECHARGE_PLAYER_" + arg_date.strftime("%Y%m%d")
    sql = ''

    exist_table_role_login = "SELECT table_name FROM information_schema.tables where table_schema = 'manager_haima' and table_name = '%s';" % role_login_str
    role_login_exist = mysql_connect.query(exist_table_role_login)
    if role_login_exist == []:
        print("创建数据库表 "+role_login_str)
        sql += "create table %s(" \
               "id bigint not null primary key auto_increment," \
               "log_time datetime not null," \
               "server_id int not null default '0'," \
               "platform_id int not null default '0'," \
               "uid char(20) not null default '0'," \
               "level int not null default '0'," \
               "vip_level int not null default '0'," \
               "install date not null,action int not null default '0'," \
               "player_name char(50) not null default ''," \
               "account_id char(50) not null default ''," \
               "account_name char(50) not null default ''," \
               "dev_id char(50) not null default ''," \
               "login_ip char(20) not null default ''," \
               "month_card_days int not null default '0'," \
               "login_dis_days int not null default '0');" % role_login_str
    exist_table_recharge_player = "SELECT table_name FROM information_schema.tables where table_schema = 'manager_haima' and table_name = '%s';" % recharge_player_str
    recharge_player_exist = mysql_connect.query(exist_table_recharge_player)
    if recharge_player_exist == []:
        print("创建数据库表 "+recharge_player_str)
        sql += "create table %s(" \
               "id bigint not null primary key auto_increment," \
               "log_time datetime not null," \
               "server_id int not null default '0'," \
               "platform_id int not null default '0'," \
               "uid char(20) not null default '0'," \
               "level int not null default '0'," \
               "vip_level int not null default '0'," \
               "install date not null," \
               "action int not null default '0'," \
               "order_id char(255) not null default ''," \
               "add_stone int not null default '0'," \
               "cur_stone int not null default '0'," \
               "shop_index int not null default '0'," \
               "shop_event int not null default '0'," \
               "old_rmb int not null default '0'," \
               "add_rmb int not null default '0'," \
               "platform_type int not null default '0'," \
               "old_stone int not null default '0'," \
               "cur_rmb int not null default '0');" % recharge_player_str
    if sql:
        mysql_connect.execute(sql)


def reset_catch_data():
    for _server_id in LOCAL_LOG_PATH_NAME_LST:
        catch_data.reset(_server_id)
        catch_data.load(_server_id)


catch_data = CatchData()


if __name__ == '__main__':
    os.chmod("/home/ubuntu/data/HaiMaLogParse/", stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
    if not os.path.exists(CHECK_PATH):
        os.makedirs(CHECK_PATH)
        os.mkdir(CHECK_PATH + 'Error')
        os.mkdir(CHECK_PATH + 'Normal')

    start_catch_logs(sys.argv)
