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
from util.logs_out_in_path import LOG_PATH
from action.parse_action import log_parse

# 日志保存路径
# 飞流mysql 飞流日志服务器地址
# CATCH_SQL_HOST = "556418a8f30f9.sh.cdb.myqcloud.com:6080"
# LOG_SERVER_PATH = "http://115.159.77.250:8086/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"

# ZGAME 海马日志服务器地址
CATCH_SQL_HOST = "555ff729cffb0.sh.cdb.myqcloud.com:6200"
LOG_SERVER_PATH = "http://115.159.69.65:8086/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"

CATCH_SQL_PAS = "Zgamecn6"

PARSE_OUT_FILE = os.getcwd() + "/parse/"
CATCH_LOGS_DAT = os.getcwd() + "/dat/save.dat"
CATCH_OUTPUT_DAT = os.getcwd() + "/dat/output.dat"
LOCAL_LOG_START_DATE = '2015-05-21'

ITEM_ACTION_LST = ['add_item_list','cost_item_list']
EQUIP_ACTION_LST = ['add_equip_list','remove_equip_list']
MONSTER_ACTION_LST = ['add_monster_list','remove_monster_list']
TREASURE_FRAGMENT_ACTION_LST = ['add_treasure_frag_list','remove_treasure_frag_list']
TREASURE_ACTION_LST = ['add_treasure_list', 'treasure_level_up_material', 'treasure_phase_up_material']

LOGIN_RECHARGE_LST = ['EVENT_ACTION_ROLE_LOGIN', 'EVENT_ACTION_RECHARGE_PLAYER']

class CatchData(object):
    # 抓取间隔时间
    catch_dis_time = 300
    #最后抓取日期
    last_catch_logs_date = None
    # 抓取行数
    last_catch_logs_line_num = 0
    # 按照日期拆分的日志
    date_logs_dict = dict()
    # 按照日志拆分的用户uid日志
    date_uid_dict = dict()
    # 按照日志拆分的设备ID日志
    date_device_id_dict = dict()
    #按照日志拆分的账号日志
    date_account_id_dict = dict()
    # mysql 队列
    mysql_queue = []


    def put(self):
        """
            保存配置
        """
        print 'put'
        out_put_file = open(CATCH_LOGS_DAT, 'w')
        dat_dict = dict()
        # dat_dict['last_catch_logs_date'] = None
        # dat_dict['last_catch_logs_line_num'] = 0
        dat_dict['last_catch_logs_date'] = self.last_catch_logs_date
        dat_dict['last_catch_logs_line_num'] = self.last_catch_logs_line_num
        pickle.dump(dat_dict, out_put_file)
        out_put_file.close()

    def load(self):
        """
            加载
        """
        if os.path.exists(CATCH_LOGS_DAT):
            out_put_file = open(CATCH_LOGS_DAT, 'r')
            dat_dict = pickle.load(out_put_file)
            print "dat_dict:"
            print dat_dict
            self.last_catch_logs_date = dat_dict['last_catch_logs_date']
            self.last_catch_logs_line_num = dat_dict['last_catch_logs_line_num']
            out_put_file.close()

catch_data = CatchData()
catch_data.load()

# 开启新进程执行
def start_catch_logs(args):

    print catch_data.last_catch_logs_date
    arg_date = datetime.date.today()
    if len(args) > 1:
        try:
            split_date_str = args[1]
            arg_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
            print "arg_date:"
            print arg_date
        except:
            sys.stderr.write("Err: Use daily_catch_split_log %Y-%m-%d")
            sys.exit(1)

        #计算起始日期
    if not catch_data.last_catch_logs_date:
        catch_data.last_catch_logs_date = arg_date
    print("抓取日期 %s 日志" % catch_data.last_catch_logs_date)
    url_path = LOG_SERVER_PATH % (catch_data.last_catch_logs_date, catch_data.last_catch_logs_date)
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
        else:
            # 是今天就记录已经加载的行数 下次增量更新
            catch_data.last_catch_logs_line_num = total_lines
        # 保存抓取状态信息
        catch_data.put()
        # time.sleep(300)


def parse_game_log(log_lines):
    """
        解析
    """
    # print("准备解析插入日志 数量" + str(len(log_lines)))
    for _log in log_lines:
        _log = _log.strip()
        log_instance = log_parse(_log)
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
        if key in ITEM_ACTION_LST:
            # print(log_dict)
            _insert_item_change_log(log_dict['uid'], log_dict['log_time'], log_dict['platform_id'], log_dict['server_id'], log_dict['action'], key, val)
        elif key in EQUIP_ACTION_LST:
            _insert_equip_change_log(log_dict['uid'], log_dict['log_time'], log_dict['platform_id'], log_dict['server_id'], log_dict['action'], key, val)
        elif key in MONSTER_ACTION_LST:
            _insert_monster_change_log(log_dict['uid'], log_dict['log_time'], log_dict['platform_id'], log_dict['server_id'], log_dict['action'], key, val)
        elif key == 'team_list':
            _insert_user_team(log_dict['uid'], log_dict['log_time'], log_dict['platform_id'], log_dict['server_id'], log_dict['team_list'])
        elif key in TREASURE_FRAGMENT_ACTION_LST:
            _insert_treasure_frag(log_dict['uid'], log_dict['log_time'], log_dict['platform_id'], log_dict['server_id'], log_dict['action'], key, val)
        elif key in TREASURE_ACTION_LST:
            _insert_treasure(log_dict['uid'], log_dict['log_time'], log_dict['platform_id'], log_dict['server_id'], log_dict['action'], key, val)
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


def _insert_treasure_frag(uid, log_time, channel_id, server_id, action, item_action,  treasure_frag_lst):
    """
        插入宝物碎片数据
    """
    if treasure_frag_lst:
        treasure_frag_lst = map(int, treasure_frag_lst)
        for index in xrange(0, len(treasure_frag_lst), 2):
            _tid = treasure_frag_lst[index]
            if item_action == TREASURE_FRAGMENT_ACTION_LST[0]:
                _num = treasure_frag_lst[index + 1]
            else:
                _num = -treasure_frag_lst[index + 1]
            sql = "INSERT INTO user_treasure_fragment_change (uid, log_time, platform_id,server_id, action, tid, num) VALUES (%s, '%s', %s, %s, %s, %s, %s);" % (uid, log_time, channel_id, server_id, action, _tid, _num)
            catch_data.mysql_queue.append(sql)


def _insert_treasure(uid, log_time, channel_id, server_id, action, item_action,  treasure_lst):
    """
        插入宝物碎片数据
    """
    if treasure_lst:
        treasure_lst = map(int, treasure_lst)
        for index in xrange(0, len(treasure_lst), 2):
            _tid = treasure_lst[index]
            if item_action == TREASURE_ACTION_LST[0]:
                _num = treasure_lst[index + 1]
            else:
                if index + 1 < len(treasure_lst):
                    _num = -treasure_lst[index + 1]
                else:
                    _num = -1

            sql = "INSERT INTO user_treasure_change (uid, log_time, platform_id,server_id, action, tid, num) VALUES (%s, '%s', %s, %s, %s, %s, %s);" % (uid, log_time, channel_id, server_id, action, _tid, _num)
            catch_data.mysql_queue.append(sql)

def _insert_user_team(uid, log_time, channel_id, server_id, team_lst):
    """
        插入玩家队伍信息
    """
    if team_lst:
        team_monster_num = len(team_lst) / 3
        monster_team_key = ""
        for index in range(0, team_monster_num):
            _num = index + 1
            monster_team_key += ",monster_%s,star_%s,level_%s" % (_num, _num, _num)
        sql = "INSERT INTO user_team (uid, log_time, platform_id, server_id %s) VALUES (%s, '%s', %s, %s, %s);" % (monster_team_key, uid, log_time, channel_id, server_id, ",".join(map(str,team_lst)))
        catch_data.mysql_queue.append(sql)


def _insert_item_change_log(uid, log_time, channel_id, server_id, action, item_action,  item_lst):
    """
        插入物品改变
        # 时间 物品ID 物品数量 用户ID 事件
    """

    if item_lst:
        item_lst = map(int, item_lst)
        for index in xrange(0, len(item_lst), 2):
            _tid = item_lst[index]

            if item_action == ITEM_ACTION_LST[0]:
                _num = item_lst[index + 1]
            else:
                _num = -item_lst[index + 1]
            sql = "INSERT INTO user_item_change (uid, log_time, platform_id,server_id, action, tid, num) VALUES (%s, '%s', %s, %s, %s, %s, %s);" % (uid, log_time, channel_id, server_id, action, _tid, _num)
            catch_data.mysql_queue.append(sql)


def _insert_equip_change_log(uid, log_time, channel_id, server_id, action, item_action,  equip_lst):
    """
        插入物品改变
        # 时间 物品ID 物品数量 用户ID 事件
    """
    if equip_lst:
        equip_lst = map(int, equip_lst)
        for index in xrange(0, len(equip_lst), 2):
            _tid = equip_lst[index]
            if item_action == EQUIP_ACTION_LST[0]:
                _num = equip_lst[index + 1]
            else:
                _num = -equip_lst[index + 1]
            sql = "INSERT INTO user_equip_change (uid, log_time, platform_id,server_id, action, tid, num) VALUES (%s, '%s', %s, %s, %s, %s, %s);" % (uid, log_time, channel_id, server_id, action, _tid, _num)
            catch_data.mysql_queue.append(sql)


def _insert_monster_change_log(uid, log_time, channel_id, server_id, action, item_action,  monster_lst):
    """
        插入物品改变
        # 时间 物品ID 物品数量 用户ID 事件
    """
    if monster_lst:
        monster_lst = map(int, monster_lst)
        for index in xrange(0, len(monster_lst), 3):
            _tid = monster_lst[index]
            _star = monster_lst[index + 1]
            if item_action == MONSTER_ACTION_LST[0]:
                _num = monster_lst[index + 2]
            else:
                _num = -monster_lst[index + 2]
            sql = "INSERT INTO user_monster_change (uid, log_time, platform_id,server_id, action, tid, star, num) VALUES (%s, '%s', %s, %s, %s, %s, %s, %s);" % (uid, log_time, channel_id, server_id, action, _tid, _star, _num)
            catch_data.mysql_queue.append(sql)


def start_insert_to_mysql():
    """
        插入mysql
    """
    mysql_connect = mysql.Connection(CATCH_SQL_HOST, 'manager', 'root', CATCH_SQL_PAS)

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


if __name__ == '__main__':
    start_catch_logs(sys.argv)


