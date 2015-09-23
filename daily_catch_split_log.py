# -*- coding:utf-8 -*-

"""
    固定每天抓取拆分日志到当前服务器
    要伴随服务器开启而开启
"""
import time
import pickle
import datetime
import sys
import os
import stat
import urllib2
import math

from mysql import mysql
from util import game_define
from action.parse_action import log_parse
from catch_split_log.GM.user_cost import _user_cost_log
from util.logs_out_in_path import LOG_PATH




# 飞流mysql 飞流日志服务器地址
# CATCH_SQL_HOST = "556418a8f30f9.sh.cdb.myqcloud.com:6080"
# LOG_SERVER_PATH = "http://115.159.77.250:8086/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"


# ZGAME 海马日志服务器地址
CATCH_SQL_HOST = "555ff729cffb0.sh.cdb.myqcloud.com:6200"
LOG_SERVER_PATH = "http://115.159.69.65:8086/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"

CATCH_SQL_PAS = "Zgamecn6"

LOCAL_LOG_START_DATE = '2015-05-21'
OUT_PUT_PATH = "/opt/GameLogParse/data/"
# OUT_PUT_PATH = os.getcwd() + "/data/"

ITEM_ACTION_LST = ['add_item_list','cost_item_list']
EQUIP_ACTION_LST = ['add_equip_list','remove_equip_list']
MONSTER_ACTION_LST = ['add_monster_list','remove_monster_list']
TREASURE_FRAGMENT_ACTION_LST = ['add_treasure_frag_list','remove_treasure_frag_list']
TREASURE_ACTION_LST = ['add_treasure_list', 'treasure_level_up_material', 'treasure_phase_up_material']


# mysql 队列
mysql_queue = []

gold_action_dict = {
    'total_cost': 0,
    'total_add': 0
}

stone_action_dict = {
    'total_cost': 0,
    'total_add': 0
}

user_level_arrive_dict = dict()
user_cur_stone_dict = dict()
user_cur_gold_dict = dict()

action_monster_lst = []
action_item_lst = []
action_equip_lst = []
all_action_log_dict = dict()
# 当天所有新安装的用户
users_new_install_set = set()
users_new_install_num = 0
# 所有活跃用户（当天登录的非新玩家）
user_active_set = set()
user_active_num = 0
# 玩家等级分布
user_level_dict = dict()
# 用户详细信息
user_detail_dict = dict()



def start(args):
    """
        获取并拆分一天的日志
    """
    # split_date = datetime.date.today() - datetime.timedelta(days=1)
    split_date = datetime.datetime.strptime("2015-5-31", "%Y-%m-%d").date()
    if len(args) > 1:
        try:
            split_date_str = args[1]
            split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
        except:
            sys.stderr.write("Err: Use daily_catch_split_log %Y-%m-%d")
            sys.exit(1)

    url_path = LOG_SERVER_PATH % (split_date, split_date)

    url = urllib2.urlopen(url_path)

    print(split_date)

    action_team_lst = []
    action_treasure_fragment_lst = []
    action_treasure_lst = []

    if url.msg == 'OK':
        global all_action_log_dict
        global user_active_set
        global users_new_install_set
        global user_level_dict
        global user_detail_dict

        # 抓取昨天的user_detail_dict
        yesterday_user_detail_file_path = OUT_PUT_PATH + str(split_date - datetime.timedelta(days=1)) + "/"
        if os.path.exists(yesterday_user_detail_file_path + 'USER_DETAIL'):
            open_file = open(yesterday_user_detail_file_path + 'USER_DETAIL', 'r')
            user_detail_dict = pickle.load(open_file)
            open_file.close()

        log_lines = url.readlines()
        log_dict_lst = []

        for _log_line in log_lines:
            _log_line = _log_line.strip()

            log_dict = log_parse(_log_line)
            log_dict_lst.append(log_dict)

            action_id = log_dict['action']
            # uid = log_dict['uid']
            action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(action_id, 'Err')

            # 插入列表 用来输出文件
            if action_str in all_action_log_dict:
                all_action_log_dict[action_str].append(log_dict)
            else:
                all_action_log_dict[action_str] = [log_dict]

            # 插入活跃用户
            if log_dict['install'] != split_date:
                user_active_set.add(log_dict['uid'])
            else:
                users_new_install_set.add(log_dict['uid'])

            # 插入玩家等级分布
            user_level = log_dict['level']
            user_uid = log_dict['uid']
            user_vip_level = log_dict['vip_level']
            user_install = log_dict['install']
            user_server_id = log_dict['server_id']
            user_platform_id = log_dict['platform_id']
            user_last_player_time = log_dict['log_time']

            if user_level > user_level_dict.get(user_uid, 0):
                user_level_dict[user_uid] = user_level

            # 插入玩家详细数据
            if user_uid in user_detail_dict:
                user_detail_dict[user_uid].update({
                    'uid': user_uid,
                    'install': user_install,
                    'server_id': user_server_id,
                    'platform_id': user_platform_id,
                    'level': user_level,
                    'vip_level': user_vip_level,
                    'last_play_time': user_last_player_time.date(),
                })
            else:
                user_detail_dict[user_uid] = {
                    'uid': user_uid,
                    'install': user_install,
                    'server_id': user_server_id,
                    'platform_id': user_platform_id,
                    'level': user_level,
                    'vip_level': user_vip_level,
                    'last_play_time': user_last_player_time.date(),
                }
            if 'cur_gold' in log_dict:
                user_detail_dict[user_uid]['gold'] = log_dict['cur_gold']
            if 'cur_stone' in log_dict:
                user_detail_dict[user_uid]['stone'] = log_dict['cur_stone']
            if 'cur_arena_emblem' in log_dict:
                user_detail_dict[user_uid]['emblem'] = log_dict['cur_arena_emblem']
            if "cur_gym_point" in log_dict:
                user_detail_dict[user_uid]['gym_point'] = log_dict['cur_gym_point']
            if 'cur_world_boss_point' in log_dict:
                user_detail_dict[user_uid]['world_boss_point'] = log_dict['cur_world_boss_point']

            # 计算玩家等级分布
            _insert_user_level_arrive_dict(log_dict)
            # 计算金币消耗产出
            _insert_gold_action(log_dict)
            # 计算钻石消耗产出
            _insert_stone_action(log_dict)
            # 计算玩家当前金币数
            _insert_user_hold_gold(log_dict)
            # 计算玩家当前钻石数
            _insert_user_hold_stone(log_dict)

            for key, val in log_dict.items():
                if key in ITEM_ACTION_LST:
                    dat = _insert_item_change_log(log_dict['uid'], log_dict['log_time'], log_dict['server_id'], log_dict['platform_id'],  log_dict['action'], log_dict['level'], key, val)
                    if dat:
                        global action_item_lst
                        action_item_lst.extend(dat)
                elif key in EQUIP_ACTION_LST:
                    dat = _insert_equip_change_log(log_dict['uid'], log_dict['log_time'], log_dict['server_id'], log_dict['platform_id'], log_dict['action'],log_dict['level'], key, val)
                    if dat:
                        global action_equip_lst
                        action_equip_lst.extend(dat)
                elif key in MONSTER_ACTION_LST:
                    dat = _insert_monster_change_log(log_dict['uid'], log_dict['log_time'], log_dict['server_id'], log_dict['platform_id'], log_dict['action'],log_dict['level'], key, val)
                    if dat:
                        global action_monster_lst
                        action_monster_lst.extend(dat)
                elif key == 'team_list':
                    dat = _insert_user_team(log_dict['uid'], log_dict['log_time'], log_dict['server_id'], log_dict['platform_id'], log_dict['team_list'])
                    if dat:
                        action_team_lst.extend(dat)
                elif key in TREASURE_FRAGMENT_ACTION_LST:
                    dat = _insert_treasure_frag(log_dict['uid'], log_dict['log_time'], log_dict['server_id'], log_dict['platform_id'], log_dict['action'], log_dict['level'], key, val)
                    if dat:
                        action_treasure_fragment_lst.extend(dat)
                elif key in TREASURE_ACTION_LST:
                    dat = _insert_treasure(log_dict['uid'], log_dict['log_time'], log_dict['server_id'], log_dict['platform_id'], log_dict['action'], log_dict['level'], key, val)
                    if dat:
                        action_treasure_lst.extend(dat)


        _calculate_global()

        os.chmod(OUT_PUT_PATH, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
        out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
        if not os.path.exists(out_put_file_path):
            os.makedirs(out_put_file_path)

        # 输出对应事件的文件
        for key, val in all_action_log_dict.items():
            out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
            print("Out: " + str(key))
            out_put_file = open(out_put_file_path + key, 'w')
            print("Pickle: " + str(key))
            pickle.dump(val, out_put_file)
            out_put_file.close()
            time.sleep(1)
        # del all_action_log_dict
        time.sleep(0.1)
        # 输出物品
        out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
        print("USER_ITEM")
        out_put_file = open(out_put_file_path + 'USER_ITEM', 'w')
        pickle.dump(action_item_lst, out_put_file)
        out_put_file.close()
        # del action_item_lst
        time.sleep(0.1)

        # 输出装备
        out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
        print("USER_EQUIP")
        out_put_file = open(out_put_file_path + 'USER_EQUIP', 'w')
        pickle.dump(action_equip_lst, out_put_file)
        out_put_file.close()
        # del action_equip_lst
        time.sleep(0.1)

        # 输出怪
        out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
        print("USER_MONSTER")
        out_put_file = open(out_put_file_path + 'USER_MONSTER', 'w')
        pickle.dump(action_monster_lst, out_put_file)
        out_put_file.close()
        # del action_monster_lst
        time.sleep(0.1)

        # 输出队伍
        out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
        print("USER_TEAM")
        out_put_file = open(out_put_file_path + 'USER_TEAM', 'w')
        pickle.dump(action_team_lst, out_put_file)
        out_put_file.close()
        # del action_team_lst
        time.sleep(0.1)

        # 宝物碎片
        out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
        print("USER_TREASURE_FRAGMENT")
        out_put_file = open(out_put_file_path + 'USER_TREASURE_FRAGMENT', 'w')
        pickle.dump(action_treasure_fragment_lst, out_put_file)
        out_put_file.close()
        # del action_treasure_fragment_lst
        time.sleep(0.1)

        # 宝物输出
        out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
        print("USER_TREASURE")
        out_put_file = open(out_put_file_path + 'USER_TREASURE', 'w')
        pickle.dump(action_treasure_lst, out_put_file)
        out_put_file.close()
        # del action_treasure_lst
        time.sleep(0.1)

        # 计算用户的游戏时间
        # uid_set = {log['uid'] for log in log_dict_lst}
        # print("USER_ONLINE_TIME")
        # uid_online_dict = dict()
        # split_datetime = datetime.datetime.strptime(str(split_date),'%Y-%m-%d')
        # for _uid in uid_set:
        #     _uid_log_lst = [log for log in log_dict_lst if log['uid'] == _uid]
        #     # 300秒内是否登录
        #     online_num = 0
        #     for _time_index in xrange(12*24):
        #         _star_datetime = split_datetime + datetime.timedelta(seconds=300) * _time_index
        #         _end_datetime = _star_datetime + datetime.timedelta(seconds=300) * _time_index
        #         if len([log for log in _uid_log_lst if _star_datetime <= log['log_time'] < _end_datetime]):
        #             online_num += 1
            # uid_online_dict[_uid] = 300 * online_num

        # out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
        # out_put_file = open(out_put_file_path + 'USER_ONLINE_TIME', 'w')
        # pickle.dump(uid_online_dict, out_put_file)
        # out_put_file.close()
        # # del uid_online_dict
        # time.sleep(0.1)

        # 输出到mysql
        _output_user_detail_to_mysql(split_date)
        # 玩家首次金币消耗
        _output_USER_FIRST_GOLD_CONSUME(split_date)
        time.sleep(0.1)
        # 玩家首次钻石消耗
        _output_USER_FIRST_STONE_CONSUME(split_date)
        time.sleep(0.1)
        # 玩家等级金币消耗
        _output_USER_GOLD_CONSUME(split_date)
        time.sleep(0.1)
        # 玩家等级钻石消耗
        _output_USER_STONE_CONSUME(split_date)
        time.sleep(0.1)
        # 玩家金币产出
        _output_USER_GENERATE_GOLD(split_date)
        time.sleep(0.1)
        # 玩家钻石产出
        _output_USER_GENERATE_STONE(split_date)
        time.sleep(0.1)
        # 玩家金币消耗
        _output_USER_COST_GOLD(split_date)
        time.sleep(0.1)
        # 玩家钻石消耗
        _output_USER_COST_STONE(split_date)
        time.sleep(0.1)
        # 玩家持有金币数
        _output_USER_HOLD_GOLD(split_date)
        time.sleep(0.1)
        # 玩家持有钻石数
        _output_USER_HOLD_STONE(split_date)
        time.sleep(0.1)
        # 玩家vip 金币消耗
        _output_USER_COST_GOLD_WITH_VIP(split_date)
        time.sleep(0.1)
        # 玩家vip 钻石消耗
        _output_USER_COST_STONE_WITH_VIP(split_date)
        time.sleep(0.1)

        # 流失分析- 玩家等级
        _output_USER_LEVEL_STATE(split_date)
        # vip分布
        # _output_VIP_DISTRIBUTED(split_date)
        # 日常钻石消费点分析
        _output_DAILY_CONSUME_DISTRIBUTED_STONE(split_date)
        # 日常金币消费点分析
        _output_DAILY_CONSUME_DISTRIBUTED_GOLD(split_date)
        # 宠物产出
        _output_CREATE_MONSTER(split_date)
        # 宠物消耗
        _output_REMOVE_MONSTER(split_date)
        # 宠物洗练
        _output_MONSTER_RESET_INDIVIDUAL(split_date)
        # 物品产出
        _output_CREATE_ITEM(split_date)
        # 物品消耗
        _output_CONSUME_ITEM(split_date)
        # 装备产出
        _output_CREATE_EQUIP(split_date)
        # 装备消耗
        _output_CONSUME_EQUIP(split_date)
        # 普通副本
        _output_NORMAL_STAGE_CHALLENGE(split_date)
        # 英雄副本
        _output_HARD_STAGE_CHALLENGE(split_date)
        # 经验副本
        _output_EXP_STAGE_CHALLENGE(split_date)
        # # 金币副本
        _output_GOLD_STAGE_CHALLENGE(split_date)
        # 试炼副本
        _output_TRIAL_STAGE_CHALLENGE(split_date)
        # 世界BOSS
        _output_WORLD_BOSS_STAGE_CHALLENGE(split_date)
        # 道场
        _output_GYM_STAGE_CHALLENGE(split_date)
        # 抓宠
        _output_CATCH_MONSTER_STAGE_CHALLENGE(split_date)
        # 夺宝副本
        _output_TREASURE_BATTLE_STAGE_CHALLENGE(split_date)
        # 钓鱼
        _output_FISHING(split_date)
        # 猜拳
        _output_FINGER_GUESS(split_date)
        # 问答 question
        _output_QUESTION(split_date)
        # 按摩
        _output_MASSAGE(split_date)
        # 进补
        _output_TONIC(split_date)

        # 用户详细信息
        _output_USER_DETAIL(split_date)

        # 玩家行为分析
        # gm_log_event.insert_gm_logs_by_uid(split_date,log_dict_lst)
        #
        # # 统计总表
        # _output_statistics_total(split_date)
        #
        # # 用户留存
        # _output_user_retain(split_date)

        #消耗统计
        _user_cost_log(log_dict_lst,split_date)


def _calculate_global():
    """
        全局数据计算
    """
    #计算活跃玩家数量
    global user_active_num
    global user_active_set
    user_active_num = len(user_active_set)

    global users_new_install_num
    global users_new_install_set
    users_new_install_num = len(users_new_install_set)


def _insert_user_level_arrive_dict(log_dict):
    """
        计算玩家等级分布
    """
    user_uid = log_dict['uid']
    if user_uid in user_level_arrive_dict:
        save_level = user_level_arrive_dict[user_uid]
        if log_dict['level'] > save_level:
            user_level_arrive_dict[user_uid] = log_dict['level']
    else:
        user_level_arrive_dict[user_uid] = log_dict['level']

def _insert_user_hold_stone(log_dict):
    """
         计算玩家拥有钻石
    """
    if 'cur_stone' in log_dict:
        global user_cur_stone_dict
        user_uid = log_dict['uid']
        cur_stone = log_dict['cur_stone']
        log_time = log_dict['log_time']

        _old_dat_dict = user_cur_stone_dict.get(user_uid, dict())
        if 'log_time' not in _old_dat_dict or _old_dat_dict.get('log_time') < log_time:
            _old_dat_dict['log_time'] = log_time
            _old_dat_dict['cur_stone'] = cur_stone
            user_cur_stone_dict[user_uid] = _old_dat_dict

def _insert_user_hold_gold(log_dict):
    """
         计算玩家拥有钻石
    """
    if 'cur_gold' in log_dict:
        global user_cur_gold_dict
        user_uid = log_dict['uid']
        cur_gold = log_dict['cur_gold']
        log_time = log_dict['log_time']

        _old_dat_dict = user_cur_gold_dict.get(user_uid, dict())
        if 'log_time' not in _old_dat_dict or _old_dat_dict.get('log_time') < log_time:
            _old_dat_dict['log_time'] = log_time
            _old_dat_dict['cur_gold'] = cur_gold
            user_cur_gold_dict[user_uid] = _old_dat_dict


def _get_arrive_level_num(_lv):
    """
         获取玩家到达等级数
    """
    return len([user_lv for user_lv in user_level_arrive_dict.values() if user_lv >= _lv])
# -----------------------------------------------------产品每日概况-----------------------------------------------
# from tables_using_sql.product_daily_analyse import statistics_total
# from tables_using_sql.product_daily_analyse import user_retain
# from tables_using_sql.user_payment_analyse import payment_point_analyse
#
#
# def _output_statistics_total(split_date):
#     print("STATISTICS_TOTAL")
#     result = statistics_total.get_table(split_date, channel_id=-1, server_id=-1)
#
#     out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
#     out_put_file = open(out_put_file_path + 'STATISTICS_TOTAL', 'w')
#     pickle.dump(result, out_put_file)
#     out_put_file.close()
#
#
# def _output_user_retain(split_date):
#     print("USER_RETAIN")
#     result = user_retain.get_table(split_date, channel_id=-1, server_id=-1)
#
#     out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
#     out_put_file = open(out_put_file_path + 'USER_RETAIN', 'w')
#     pickle.dump(result, out_put_file)
#     out_put_file.close()
#
#
# def _output_payment_point_analyse(split_date):
#     print("PAYMENT_POINT_ANALYSE")
#     result = payment_point_analyse.get_table(split_date, channel_id=-1, server_id=-1)
#
#     out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
#     out_put_file = open(out_put_file_path + 'PAYMENT_POINT_ANALYSE', 'w')
#     pickle.dump(result, out_put_file)
#     out_put_file.close()


# -----------------------------------------------------用户统计-----------------------------------------------
def _output_user_detail_to_mysql(split_date):
    """
        输出用户详细信息到mysql
    """
    # 整合mysql语句
    for user_dict in user_detail_dict.values():
        if user_dict['install'] == split_date:
            key_lst = user_dict.keys()
            val_lst = [user_dict[key] for key in key_lst]
            for index in xrange(len(val_lst)):
                val = val_lst[index]
                if isinstance(val, datetime.datetime) or isinstance(val, datetime.date):
                    val_lst[index] = "'%s'" % str(val)
                else:
                    val_lst[index] = str(val)

            key_str = ','.join(key_lst)
            val_str = ','.join(val_lst)
            sql = "INSERT INTO user_detail (%s) VALUES (%s);" % (key_str, val_str)
            mysql_queue.append(sql)
        else:
            key_lst = user_dict.keys()
            val_lst = [user_dict[key] for key in key_lst]
            for index in xrange(len(val_lst)):
                val = val_lst[index]
                if isinstance(val, datetime.datetime) or isinstance(val, datetime.date):
                    val_lst[index] = "'%s'" % str(val)
                else:
                    val_lst[index] = str(val)

            key_val_lst = []
            for index in xrange(len(key_lst)):
                _key = key_lst[index]
                _val = val_lst[index]
                key_val = "%s=%s" % (_key, _val)
                key_val_lst.append(key_val)

            key_val_str = ', '.join(key_val_lst)
            sql = "UPDATE user_detail SET %s WHERE uid=%s;" % (key_val_str, user_dict['uid'])
            mysql_queue.append(sql)
    _start_insert_to_mysql()


def _output_USER_DETAIL(split_date):
    """
        输出用户详细信息
    """
    print("USER_DETAIL")
    global user_detail_dict
    _user_detail_dict = user_detail_dict

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'USER_DETAIL', 'w')
    pickle.dump(_user_detail_dict, out_put_file)
    out_put_file.close()


def _output_USER_LEVEL_STATE(split_date):
    """
        用户等级分布
        # 登录用户数  新增用户数  等级用户数
    """
    print("USER_LEVEL_STATE")
    global users_new_install_num
    global user_active_num
    result = []
    new_user_num = users_new_install_num
    active_num = user_active_num
    # 登录用户数
    login_user_num = active_num + new_user_num
    result.append(login_user_num)
    result.append(new_user_num)

    # 等级用户数
    for lv in xrange(1, 121):
        _user_num = 0
        for _l in user_level_dict.values():
            if _l == lv:
                _user_num += 1
        result.append(_user_num)

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'USER_LEVEL_STATE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_VIP_DISTRIBUTED(split_date):
    """
        用户VIP分布
        条件	首冲	月卡	vip0	vip1	vip2	vip3	vip4	vip5	vip6	vip7	vip8	vip9	vip10	vip11	vip12
    """
    print("VIP_DISTRIBUTED")
    global user_detail_dict
    global users_new_install_num

    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_RECHARGE_PLAYER, 'Err')
    recharge_logs = all_action_log_dict.get(action_str, [])

    _user_detail_dict = user_detail_dict
    _install_num = users_new_install_num

    # print len([dat['install'] for dat in _user_detail_dict.values() if dat['vip_level'] == 0])
    # print len([dat['install'] for dat in _user_detail_dict.values() if dat['vip_level'] == 0 and dat['install'] == split_date])
    # 首冲
    first_recharge = len(set([log['uid'] for log in recharge_logs if log['old_rmb'] == 0]))
    # 月卡
    month_card_recharge = len(set([log['uid'] for log in recharge_logs if log['shop_index'] == 1]))
    # vip总体登录
    total_line = ['总体登录', first_recharge, month_card_recharge]

    # 不带注册
    # for _vip_lv in xrange(13):
    #     user_num = len([dat['uid'] for dat in _user_detail_dict.values() if dat['vip_level'] == _vip_lv])
    #     total_line.append(user_num)
    # print _user_detail_dict.values()

    # 注册时间VIP分布
    total_line_dict = dict()
    total_line_dict['Total'] = [0] * 13
    for item in _user_detail_dict.values():
        install = item['install'].strftime('%Y-%m-%d')
        if install not in total_line_dict.keys():
            total_line_dict[install] = [0] * 13
            total_line_dict[install][item['vip_level']] += 1
            total_line_dict['Total'][item['vip_level']] += 1
        else:
            total_line_dict[install][item['vip_level']] += 1
            total_line_dict['Total'][item['vip_level']] += 1
    total_line_dict['cur_date'] = split_date
    # print "total_line_dict:"
    # print total_line_dict

    #------------ 新增部分---------
    add_line = ['新增角色数']
    add_line.extend([_install_num] * 15)

    # 首冲
    first_recharge = len(set([log['uid'] for log in recharge_logs if log['old_rmb'] == 0 and log['install'] == split_date]))
    # 月卡
    month_card_recharge = len(set([log['uid'] for log in recharge_logs if log['shop_index'] == 1 and log['install'] == split_date]))
    # vip 新增充值
    new_user_line = ['新增充值', first_recharge, month_card_recharge]

    for _vip_lv in xrange(13):
        new_user_num = len([dat['uid'] for dat in _user_detail_dict.values() if dat['vip_level'] == _vip_lv and dat['install'] == split_date])
        new_user_line.append(new_user_num)

    rate_line = ['比率']

    for _index in xrange(1, 16):
        rate = round(float(new_user_line[_index])/ float(add_line[_index]), 2)
        rate_line.append(str(rate*100)+'%')

    result = [
        total_line,
        new_user_line,
        add_line,
        rate_line,
        total_line_dict,
    ]
    # print "result:"
    # print result
    # 输出VIP 分布
    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'VIP_DISTRIBUTED', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


# def _output_VIP_DISTRIBUTED_WITH_REGISTER(split_date):
#     global user_detail_dict
#     _user_detail_dict = user_detail_dict
#     total_line = []
#     result = dict()
#     for _vip_lv in xrange(13):
#         new_user_num = len([dat['uid'] for dat in _user_detail_dict.values() if dat['vip_level'] == _vip_lv and dat['install'] == split_date])
#         total_line.append(new_user_num)
#     result['split_date'] = total_line
#     # 输出VIP分布中的总体登录
#     out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
#     out_put_file = open(out_put_file_path + 'VIP_DISTRIBUTED', 'w')
#     pickle.dump(result, out_put_file)
#     out_put_file.close()
# --------------------------------------------------活动模块分析------------------------------------------------------
def _output_FISHING(split_date):
    """
        钓鱼
        参与人数	总钓鱼次数	到达要求人数	参与率
    """
    print("FISHING")
    fishing_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_FISHING_ONCE, 'Err')
    fishing_logs.extend(all_action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_FISHING_LOOP, 'Err')
    fishing_logs.extend(all_action_log_dict.get(action_str, []))

    join_user_num = len(set([log['uid'] for log in fishing_logs]))

    fishing_count = sum([log['cost_fishing_count'] for log in fishing_logs])

    can_join_user_num = len(set([_uid for _uid, _lv in user_level_dict.items() if _lv >= 15]))

    rate = round(float(join_user_num)/ float(can_join_user_num), 2)

    result = [join_user_num, fishing_count, can_join_user_num, rate]

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'FISHING', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_FINGER_GUESS(split_date):
    """
        猜拳
        参与人数	总次数	到达要求人数	参与率
    """
    print("FINGER_GUESS")
    finger_guess_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_FINGER_GUESS_EXCHANGE, 'Err')
    finger_guess_logs.extend(all_action_log_dict.get(action_str, []))

    join_user_num = len(set([log['uid'] for log in finger_guess_logs]))

    finger_guess_count = len(finger_guess_logs)

    can_join_user_num = len(set([_uid for _uid, _lv in user_level_dict.items() if _lv >= 13]))

    rate = round(float(join_user_num)/ float(can_join_user_num), 2)

    result = [join_user_num, finger_guess_count, can_join_user_num, rate]

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'FINGER_GUESS', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_QUESTION(split_date):
    """
        问答
        参与人数	总次数	到达要求人数	参与率
    """
    print("QUESTION")
    question_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_QUIZ_ANSWER_TRUE, 'Err')
    question_logs.extend(all_action_log_dict.get(action_str, []))

    join_user_num = len(set([log['uid'] for log in question_logs]))

    _count = len(question_logs)

    can_join_user_num = len(set([_uid for _uid, _lv in user_level_dict.items() if _lv >= 26]))

    rate = round(float(join_user_num)/ float(can_join_user_num), 2)

    result = [join_user_num, _count, can_join_user_num, rate]

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'QUESTION', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()



def _output_TONIC(split_date):
    """
        进补
        参与人数	总次数	到达要求人数	参与率
    """
    print("TONIC")
    question_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_GET_TONIC, 'Err')
    question_logs.extend(all_action_log_dict.get(action_str, []))

    join_user_num = len(set([log['uid'] for log in question_logs]))

    _count = len(question_logs)

    can_join_user_num = len(set([_uid for _uid, _lv in user_level_dict.items() if _lv >= 1]))

    rate = round(float(join_user_num)/ float(can_join_user_num), 2)

    result = [join_user_num, _count, can_join_user_num, rate]

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'TONIC', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

def _output_MASSAGE(split_date):
    """
        按摩
        参与人数	总次数	到达要求人数	参与率
    """
    print("MASSAGE")
    massage_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_MASSAGE_REWARD, 'Err')
    massage_logs.extend(all_action_log_dict.get(action_str, []))

    join_user_num = len(set([log['uid'] for log in massage_logs]))

    _count = len(massage_logs)

    can_join_user_num = len(set([_uid for _uid, _lv in user_level_dict.items() if _lv >= 1]))

    rate = round(float(join_user_num)/ float(can_join_user_num), 2)

    result = [join_user_num, _count, can_join_user_num, rate]

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'MASSAGE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


# --------------------------------------------------副本进度------------------------------------------------------
def _output_NORMAL_STAGE_CHALLENGE(split_date):
    """
        普通关卡挑战数据
         # 副本名称	挑战数	通过数	扫荡次数	成功率
    """
    print("NORMAL_STAGE_CHALLENGE")
    normal_stage_logs = []
    mop_stage_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_NORMAL_FAIL, 'Err')
    normal_stage_logs.extend(all_action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_NORMAL_WIN, 'Err')
    normal_stage_logs.extend(all_action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_MOP, 'Err')
    mop_stage_logs.extend(all_action_log_dict.get(action_str, []))

    # 胜利失败关卡日志字典
    stage_id_logs_dict = dict()
    for _log in normal_stage_logs:
        _stage_id = _log['stage_index']
        _dat_lst = stage_id_logs_dict.get(_stage_id, [])
        _dat_lst.append(_log)
        stage_id_logs_dict[_stage_id] = _dat_lst

    # 扫荡关卡字典
    mop_stage_id_logs_dict = dict()
    for _log in mop_stage_logs:
        _stage_id = _log['stage_index']
        _dat_lst = mop_stage_id_logs_dict.get(_stage_id, [])
        _dat_lst.append(_log)
        mop_stage_id_logs_dict[_stage_id] = _dat_lst

    result = []
    for _stage_id, logs in stage_id_logs_dict.items():

        # 挑战数
        challenge_count = len(logs)
        # 通过数
        challenge_win_count = len([l for l in logs if l['action'] == game_define.EVENT_ACTION_STAGE_NORMAL_WIN])
        # 扫荡次数
        mop_count = len(mop_stage_id_logs_dict.get(_stage_id, []))
        #胜率
        win_rate = round(float(challenge_win_count)/float(challenge_count), 2)

        result.append([_stage_id, challenge_count, challenge_win_count, mop_count, win_rate])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'NORMAL_STAGE_CHALLENGE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_HARD_STAGE_CHALLENGE(split_date):
    """
        困难关卡挑战
        # 副本名称	挑战数	通过数	扫荡次数	成功率
    """
    print("HARD_STAGE_CHALLENGE")
    hero_stage_logs = []
    mop_stage_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_HERO_FAIL, 'Err')
    hero_stage_logs.extend(all_action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_HERO_WIN, 'Err')
    hero_stage_logs.extend(all_action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_MOP, 'Err')
    mop_stage_logs.extend(all_action_log_dict.get(action_str, []))

    # 胜利失败关卡日志字典
    stage_id_logs_dict = dict()
    for _log in hero_stage_logs:
        _stage_id = _log['stage_index']
        _dat_lst = stage_id_logs_dict.get(_stage_id, [])
        _dat_lst.append(_log)
        stage_id_logs_dict[_stage_id] = _dat_lst

    # 扫荡关卡字典
    mop_stage_id_logs_dict = dict()
    for _log in mop_stage_logs:
        _stage_id = _log['stage_index']
        _dat_lst = mop_stage_id_logs_dict.get(_stage_id, [])
        _dat_lst.append(_log)
        mop_stage_id_logs_dict[_stage_id] = _dat_lst

    result = []
    for _stage_id, logs in stage_id_logs_dict.items():

        # 挑战数
        challenge_count = len(logs)
        # 通过数
        challenge_win_count = len([l for l in logs if l['action'] == game_define.EVENT_ACTION_STAGE_HERO_WIN])
        # 扫荡次数
        mop_count = len(mop_stage_id_logs_dict.get(_stage_id, []))
        #胜率
        win_rate = round(float(challenge_win_count)/float(challenge_count), 2)

        result.append([_stage_id, challenge_count, challenge_win_count, mop_count, win_rate])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'HARD_STAGE_CHALLENGE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_EXP_STAGE_CHALLENGE(split_date):
    """
        经验关卡挑战数据
         # 参与人数 参与次数  完成人数 总完成次数 到达要求人数 参与率 成功率

    """
    print("EXP_STAGE_CHALLENGE")
    normal_stage_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_EXP_WIN, 'Err')
    normal_stage_logs.extend(all_action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_EXP_FAIL, 'Err')
    normal_stage_logs.extend(all_action_log_dict.get(action_str, []))


    # 胜利失败关卡日志字典
    stage_id_logs_dict = dict()
    for _log in normal_stage_logs:
        _stage_id = _log['stage_index']
        _dat_lst = stage_id_logs_dict.get(_stage_id, [])
        _dat_lst.append(_log)
        stage_id_logs_dict[_stage_id] = _dat_lst

    can_join_user_num = len(set([_uid for _uid, _lv in user_level_dict.items() if _lv >= 27]))

    result = []
    for _stage_id, logs in stage_id_logs_dict.items():
        # 参与人数
        challenge_user_count = len(set([l['uid'] for l in logs]))
        # 参与次数
        challenge_count = len(logs)
        # 总完成次数
        challenge_win_count = len([l for l in logs if l['action'] == game_define.EVENT_ACTION_STAGE_EXP_WIN])
        # 完成人数
        challenge_win_user_count = len(set([l['uid'] for l in logs if l['action'] == game_define.EVENT_ACTION_STAGE_EXP_WIN]))
        #胜率
        win_rate = round(float(challenge_win_count)/float(challenge_count), 2)

        # 参与率
        join_rate = round(float(challenge_user_count)/float(can_join_user_num), 2)
        result.append([_stage_id, challenge_user_count, challenge_count,  challenge_win_user_count, challenge_win_count, can_join_user_num, join_rate, win_rate])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'EXP_STAGE_CHALLENGE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_GOLD_STAGE_CHALLENGE(split_date):
    """
        经验关卡挑战数据
         # 参与人数 参与次数  完成人数 总完成次数 到达要求人数 参与率 成功率

    """
    print("GOLD_STAGE_CHALLENGE")
    normal_stage_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_GOLD_WIN, 'Err')
    normal_stage_logs.extend(all_action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_GOLD_FAIL, 'Err')
    normal_stage_logs.extend(all_action_log_dict.get(action_str, []))

    # 胜利失败关卡日志字典
    stage_id_logs_dict = dict()
    for _log in normal_stage_logs:
        _stage_id = _log['stage_index']
        _dat_lst = stage_id_logs_dict.get(_stage_id, [])
        _dat_lst.append(_log)
        stage_id_logs_dict[_stage_id] = _dat_lst

    can_join_user_num = len(set([_uid for _uid, _lv in user_level_dict.items() if _lv >= 29]))

    result = []
    for _stage_id, logs in stage_id_logs_dict.items():
        # 参与人数
        challenge_user_count = len(set([l['uid'] for l in logs]))
        # 参与次数
        challenge_count = len(logs)
        # 总完成次数
        challenge_win_count = len([l for l in logs if l['action'] == game_define.EVENT_ACTION_STAGE_GOLD_WIN])
        # 完成人数
        challenge_win_user_count = len(set([l['uid'] for l in logs if l['action'] == game_define.EVENT_ACTION_STAGE_GOLD_WIN]))
        #胜率
        win_rate = round(float(challenge_win_count)/float(challenge_count), 2)

        # 参与率
        join_rate = round(float(challenge_user_count)/float(can_join_user_num), 2)
        result.append([_stage_id, challenge_user_count, challenge_count,  challenge_win_user_count, challenge_win_count, can_join_user_num, join_rate, win_rate])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'GOLD_STAGE_CHALLENGE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_GYM_STAGE_CHALLENGE(split_date):
    """
        经验关卡挑战数据
         # 参与人数 参与次数  完成人数 总完成次数 到达要求人数 参与率 成功率
    """
    print("GYM_STAGE_CHALLENGE")
    stage_logs = []
    mop_stage_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_GYM_FAIL, 'Err')
    stage_logs.extend(all_action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_GYM_WIN, 'Err')
    stage_logs.extend(all_action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_GYM_MOP, 'Err')
    mop_stage_logs.extend(all_action_log_dict.get(action_str, []))
    # if len(stage_logs) > 1:
    #  print ("GYM_STAGE_CHALLENGE len is : "+ str(len(stage_logs)) + str(stage_logs[0]))
    # 胜利失败关卡日志字典
    can_join_user_num = len(set([_uid for _uid, _lv in user_level_dict.items() if _lv >= 18]))

    result = []
    # 参与人数
    challenge_user_count = len(set([l['uid'] for l in stage_logs]))
    # 参与次数
    challenge_count = len(stage_logs)
    # 总完成次数
    challenge_win_count = len([l for l in stage_logs if l['action'] == game_define.EVENT_ACTION_GYM_WIN])
    # 完成人数
    challenge_win_user_count = len(set([l['uid'] for l in stage_logs if l['action'] == game_define.EVENT_ACTION_GYM_WIN]))
    # 扫荡次数
    mop_count = len(mop_stage_logs)
    #胜率
    win_rate = round(float(challenge_win_count)/float(challenge_count), 2)

    # 参与率
    join_rate = round(float(challenge_user_count)/float(can_join_user_num), 2)
    result.append([challenge_user_count, challenge_count,  challenge_win_user_count, challenge_win_count, can_join_user_num, mop_count, join_rate, win_rate])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'GYM_STAGE_CHALLENGE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_CATCH_MONSTER_STAGE_CHALLENGE(split_date):
    """
        经验关卡挑战数据
         # 参与人数 参与次数  完成人数 总完成次数 到达要求人数 参与率 成功率
    """
    print("CATCH_MONSTER_STAGE_CHALLENGE")
    stage_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_GET_CATCH_MONSTER_RESULT, 'Err')
    stage_logs.extend(all_action_log_dict.get(action_str, []))

    # 胜利失败关卡日志字典
    can_join_user_num = len(set([_uid for _uid, _lv in user_level_dict.items() if _lv >= 31]))

    result = []
    # 参与人数
    challenge_user_count = len(set([l['uid'] for l in stage_logs]))
    # 参与次数
    challenge_count = len(stage_logs)
    # 总完成次数
    challenge_win_count = len([l for l in stage_logs if l['action'] == game_define.EVENT_ACTION_GET_CATCH_MONSTER_RESULT])
    # 完成人数
    challenge_win_user_count = len(set([l['uid'] for l in stage_logs if l['action'] == game_define.EVENT_ACTION_GET_CATCH_MONSTER_RESULT]))
    #胜率
    win_rate = round(float(challenge_win_count)/float(challenge_count), 2)

    # 参与率
    join_rate = round(float(challenge_user_count)/float(can_join_user_num), 2)
    result.append([challenge_user_count, challenge_count,  challenge_win_user_count, challenge_win_count, can_join_user_num, join_rate, win_rate])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'CATCH_MONSTER_STAGE_CHALLENGE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_TRIAL_STAGE_CHALLENGE(split_date):
    """
        经验关卡挑战数据
         # 参与人数 参与次数  完成人数 总完成次数 到达要求人数 参与率 成功率

    """
    print("TRIAL_STAGE_CHALLENGE")
    stage_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_TRIAL_BATTLE_FAIL, 'Err')
    stage_logs.extend(all_action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_TRIAL_BATTLE_WIN, 'Err')
    stage_logs.extend(all_action_log_dict.get(action_str, []))

    # 胜利失败关卡日志字典
    can_join_user_num = len(set([_uid for _uid, _lv in user_level_dict.items() if _lv >= 34]))

    result = []
    # 参与人数
    challenge_user_count = len(set([l['uid'] for l in stage_logs]))
    # 参与次数
    challenge_count = len(stage_logs)
    # 总完成次数
    challenge_win_count = len([l for l in stage_logs if l['action'] == game_define.EVENT_ACTION_TRIAL_BATTLE_WIN])
    # 完成人数
    challenge_win_user_count = len(set([l['uid'] for l in stage_logs if l['action'] == game_define.EVENT_ACTION_TRIAL_BATTLE_WIN]))
    #胜率
    win_rate = round(float(challenge_win_count)/float(challenge_count), 2)

    # 参与率
    join_rate = round(float(challenge_user_count)/float(can_join_user_num), 2)
    result.append([challenge_user_count, challenge_count,  challenge_win_user_count, challenge_win_count, can_join_user_num, join_rate, win_rate])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'TRIAL_STAGE_CHALLENGE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_WORLD_BOSS_STAGE_CHALLENGE(split_date):
    """
        经验关卡挑战数据
         # 参与人数 参与次数  完成人数 总完成次数 到达要求人数 参与率 成功率

    """
    print("WORLD_BOSS_STAGE_CHALLENGE")
    stage_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_WORLD_BOSS_ATTACK, 'Err')
    stage_logs.extend(all_action_log_dict.get(action_str, []))

    # 胜利失败关卡日志字典
    can_join_user_num = len(set([_uid for _uid, _lv in user_level_dict.items() if _lv >= 32]))

    result = []
    # 参与人数
    challenge_user_count = len(set([l['uid'] for l in stage_logs]))
    # 参与次数
    challenge_count = len(stage_logs)
    # 总完成次数
    challenge_win_count = len([l for l in stage_logs if l['action'] == game_define.EVENT_ACTION_WORLD_BOSS_ATTACK])
    # 完成人数
    challenge_win_user_count = len(set([l['uid'] for l in stage_logs if l['action'] == game_define.EVENT_ACTION_WORLD_BOSS_ATTACK]))
    #胜率
    win_rate = round(float(challenge_win_count)/float(challenge_count), 2)

    # 参与率
    join_rate = round(float(challenge_user_count)/float(can_join_user_num), 2)
    result.append([challenge_user_count, challenge_count,  challenge_win_user_count, challenge_win_count, can_join_user_num, join_rate, win_rate])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'WORLD_BOSS_STAGE_CHALLENGE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_TREASURE_BATTLE_STAGE_CHALLENGE(split_date):
    """
        夺宝关卡挑战数据
         # 参与人数 参与次数  完成人数 总完成次数 到达要求人数 参与率 成功率
    """
    print("TREASURE_BATTLE_STAGE_CHALLENGE")
    stage_logs = []
    mop_stage_logs = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_TREASURE_BATTLE_FAIL, 'Err')
    stage_logs.extend(all_action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_TREASURE_BATTLE_WIN, 'Err')
    stage_logs.extend(all_action_log_dict.get(action_str, []))
    # action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STAGE_MOP, 'Err')#扫荡
    # mop_stage_logs.extend(all_action_log_dict.get(action_str, []))
    # if len(stage_logs) > 1:
     # print ("TREASURE_BATTLE_STAGE len is : "+ str(len(stage_logs)) + str(stage_logs[0]))
    # 胜利失败关卡日志字典
    can_join_user_num = len(set([_uid for _uid, _lv in user_level_dict.items() if _lv >= 18]))
    # print can_join_user_num
    result = []
    # 参与人数
    challenge_user_count = len(set([l['uid'] for l in stage_logs]))
    # 参与次数
    challenge_count = len(stage_logs)
    # 总完成次数
    challenge_win_count = len([l for l in stage_logs if l['action'] == game_define.EVENT_ACTION_TREASURE_BATTLE_WIN])
    # 完成人数
    challenge_win_user_count = len(set([l['uid'] for l in stage_logs if l['action'] == game_define.EVENT_ACTION_TREASURE_BATTLE_WIN]))
    # 扫荡次数
    # mop_count = len(mop_stage_logs)
    #胜率
    win_rate = round(float(challenge_win_count)/float(challenge_count), 2)

    # 参与率
    join_rate = round(float(challenge_user_count)/float(can_join_user_num), 2)
    result.append([challenge_user_count, challenge_count,  challenge_win_user_count, challenge_win_count, can_join_user_num, join_rate, win_rate])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'TREASURE_BATTLE_STAGE_CHALLENGE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

# --------------------------------------------------装备相关统计------------------------------------------------------
def _output_CREATE_EQUIP(split_date):
    """
        装备产出
    """
    print("CREATE_EQUIP")
    global action_equip_lst
    _create_equip = dict()
    for log in action_equip_lst:
        _num = log['num']
        if _num > 0:
            _item_tid = log['tid']
            _action = log['action']
            action_num_dict = _create_equip.get(_item_tid, dict())
            action_num_dict[_action] = action_num_dict.get(_action, 0) + 1 * _num
            _create_equip[_item_tid] = action_num_dict
    result = []
    for _tid, _action_num_dict in _create_equip.items():
        result.append([_tid, _action_num_dict])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'CREATE_EQUIP', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_CONSUME_EQUIP(split_date):
    """
        装备消耗
    """
    print("CONSUME_EQUIP")
    global action_equip_lst
    _create_equip = dict()
    for log in action_equip_lst:
        _num = log['num']
        if _num < 0:
            _item_tid = log['tid']
            _action = log['action']
            action_num_dict = _create_equip.get(_item_tid, dict())
            action_num_dict[_action] = action_num_dict.get(_action, 0) + 1 * int(math.fabs(_num))
            _create_equip[_item_tid] = action_num_dict
    result = []
    for _tid, _action_num_dict in _create_equip.items():
        result.append([_tid, _action_num_dict])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'CONSUME_EQUIP', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

# --------------------------------------------------物品相关统计------------------------------------------------------
def _output_CREATE_ITEM(split_date):
    """
        物品产出
        {"uid": uid, "log_time": log_time, "channel_id":channel_id, "server_id":server_id, "action":action, "level": level, "tid":_tid, "num":_num}
    """
    print("CREATE_ITEM")
    global action_item_lst
    _create_item = dict()
    for log in action_item_lst:
        _num = log['num']
        if _num > 0:
            _item_tid = log['tid']
            _action = log['action']
            action_num_dict = _create_item.get(_item_tid, dict())
            action_num_dict[_action] = action_num_dict.get(_action, 0) + 1 * _num
            _create_item[_item_tid] = action_num_dict
    result = []
    for _tid, _action_num_dict in _create_item.items():
        result.append([_tid, _action_num_dict])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'CREATE_ITEM', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

def _output_CONSUME_ITEM(split_date):
    """
        物品消耗
    """
    print("CONSUME_ITEM")
    global action_item_lst
    _create_item = dict()
    for log in action_item_lst:
        _num = log['num']
        if _num < 0:
            _item_tid = log['tid']
            _action = log['action']
            action_num_dict = _create_item.get(_item_tid, dict())
            action_num_dict[_action] = action_num_dict.get(_action, 0) + 1 * int(math.fabs(_num))
            _create_item[_item_tid] = action_num_dict
    result = []
    for _tid, _action_num_dict in _create_item.items():
        result.append([_tid, _action_num_dict])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'CONSUME_ITEM', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

# --------------------------------------------------宠物相关统计------------------------------------------------------
def _output_CREATE_MONSTER(split_date):
    """
        宠物产出
        宠物 星级 action...

    """
    print("CREATE_MONSTER")
    global action_monster_lst
    _create_monster = dict()
    for log in action_monster_lst:
        _num = log['num']
        if _num > 0:
            _monster_tid = log['tid']
            _star = log['star']
            _action = log['action']
            key_monster = "%s_%s" % (_monster_tid, _star)
            action_num_dict = _create_monster.get(key_monster, dict())
            action_num_dict[_action] = action_num_dict.get(_action, 0) + 1 * _num
            _create_monster[key_monster] = action_num_dict
    result = []
    for key, _action_num_dict in _create_monster.items():
        key_lst = map(int, key.split('_'))
        _tid = key_lst[0]
        _star = key_lst[1]
        result.append([_tid, _star, _action_num_dict])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'CREATE_MONSTER', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

def _output_REMOVE_MONSTER(split_date):
    """
        宠物消耗
    """
    print("REMOVE_MONSTER")
    global action_monster_lst
    _create_monster = dict()
    for log in action_monster_lst:
        _num = log['num']
        if _num < 0:

            _monster_tid = log['tid']
            _star = log['star']
            _action = log['action']
            key_monster = "%s_%s" % (_monster_tid, _star)
            action_num_dict = _create_monster.get(key_monster, dict())
            action_num_dict[_action] = action_num_dict.get(_action, 0) + 1 * int(math.fabs(_num))
            _create_monster[key_monster] = action_num_dict
    result = []
    for key, _action_num_dict in _create_monster.items():
        key_lst = map(int, key.split('_'))
        _tid = key_lst[0]
        _star = key_lst[1]
        result.append([_tid, _star, _action_num_dict])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'REMOVE_MONSTER', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

def _output_MONSTER_RESET_INDIVIDUAL(split_date):
    """
        宠物洗练
        # 宠物  {uid_}
        [_name, reset_50_user_num, reset_50_100_user_num, reset_100_200_user_num, reset_200_400_user_num, reset_400_800_user_num, reset_up_800_user_num]
    """
    print("MONSTER_RESET_INDIVIDUAL")
    global all_action_log_dict
    reset_individual_log_lst = []
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_RESET_INDIVIDUAL_MONSTER, 'Err')
    reset_individual_log_lst.extend(all_action_log_dict.get(action_str, []))
    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_STONE_RESET_INDIVIDUAL_MONSTER, 'Err')
    reset_individual_log_lst.extend(all_action_log_dict.get(action_str, []))

    _dat = dict()
    for _log in reset_individual_log_lst:
        _monster_tid = _log['monster_tid']
        _user_uid = _log['uid']
        _user_reset_dict = _dat.get(_monster_tid, dict())
        _user_reset_dict[_user_uid] = _user_reset_dict.get(_user_uid, 0) + 1
        _dat[_monster_tid] = _user_reset_dict

    result = []
    for _tid, _user_reset_dict in _dat.items():
        less_50 = 0
        in_50_100 = 0
        in_100_200 = 0
        in_200_400 = 0
        in_400_800 = 0
        up_800 = 0
        for _num in _user_reset_dict.values():
            if _num < 50:
                less_50 += 1
            elif 50 <= _num < 100:
                in_50_100 += 1
            elif 100 <= _num < 200:
                in_100_200 += 1
            elif 200 <= _num < 400:
                in_200_400 += 1
            elif 400 <= _num < 800:
                in_400_800 += 1
            elif 800 <= _num:
                up_800 += 1

        result.append([_tid, less_50, in_50_100, in_100_200, in_200_400, in_400_800, up_800])

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'MONSTER_RESET_INDIVIDUAL', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

# --------------------------------------------------数值平衡------------------------------------------------------
def _output_USER_FIRST_GOLD_CONSUME(split_date):
    """
        玩家首次消耗数据
    """
    print("USER_FIRST_GOLD_CONSUME")
    key_first_cost_action_set = 'first_cost_action_set'
    action_set = gold_action_dict[key_first_cost_action_set]

    total_cost_gold = gold_action_dict["first_total_cost"]

    action_user_num_dict = dict()
    action_total_gold_dict = dict()
    for _action in action_set:
        # 事件消耗金币数
        key_first_cost_total_gold = 'first_cost_%s' % _action
        action_total_gold_dict[_action] = gold_action_dict[key_first_cost_total_gold]
        # 事件人数
        key_first_cost_user_set = 'first_cost_user_set_%s' % _action
        user_set = gold_action_dict[key_first_cost_user_set]
        action_user_num_dict[_action] = len(user_set)

    total_user_num = sum(action_user_num_dict.values())
    result = []
    for _action in action_set:
        _action_total_cost_gold = action_total_gold_dict[_action]
        _action_user_num = action_user_num_dict[_action]
        _user_num_rate = round(float(_action_user_num) / float(total_user_num), 2)
        _gold_rate =  round(float(_action_total_cost_gold) / float(total_cost_gold), 2)
        _dat = dict()
        _dat['action'] = _action
        _dat['gold_num'] = _action_total_cost_gold
        _dat['user_num'] = _action_user_num
        _dat['user_rate'] = _user_num_rate
        _dat['gold_rate'] = _gold_rate
        result.append(_dat)
    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'USER_FIRST_GOLD_CONSUME', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

def _output_USER_FIRST_STONE_CONSUME(split_date):
    """
        玩家首次钻石消耗数据
    """
    print("USER_FIRST_STONE_CONSUME")
    key_first_cost_action_set = 'first_cost_action_set'
    action_set = stone_action_dict[key_first_cost_action_set]

    total_cost_stone = stone_action_dict["first_total_cost"]

    action_user_num_dict = dict()
    action_total_stone_dict = dict()
    for _action in action_set:
        # 事件消耗金币数
        key_first_cost_total_stone = 'first_cost_%s' % _action
        action_total_stone_dict[_action] = stone_action_dict[key_first_cost_total_stone]
        # 事件人数
        key_first_cost_user_set = 'first_cost_user_set_%s' % _action
        user_set = stone_action_dict[key_first_cost_user_set]
        action_user_num_dict[_action] = len(user_set)

    total_user_num = sum(action_user_num_dict.values())
    result = []
    for _action in action_set:
        _action_total_cost_stone = action_total_stone_dict[_action]
        _action_user_num = action_user_num_dict[_action]
        _user_num_rate = round(float(_action_user_num) / float(total_user_num), 2)
        _stone_rate = round(float(_action_total_cost_stone) / float(total_cost_stone), 2)
        _dat = dict()
        _dat['action'] = _action
        _dat['stone_num'] = _action_total_cost_stone
        _dat['user_num'] = _action_user_num
        _dat['user_rate'] = _user_num_rate
        _dat['stone_rate'] = _stone_rate
        result.append(_dat)
    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'USER_FIRST_STONE_CONSUME', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

def _output_USER_GOLD_CONSUME(split_date):
    """
        输出用户金币消耗部分数据
    """
    print("USER_GOLD_CONSUME")
    # 计算等级消耗表数据
    for _lv in xrange(1, 121):
        level_cost_key = 'level_user_cost_set_%s' % _lv

        if level_cost_key in gold_action_dict:
            cost_user_num = len(gold_action_dict[level_cost_key])
            gold_action_dict['level_user_cost_num_%s' % _lv] = cost_user_num
            gold_action_dict['level_arppu_%s' % _lv] = round(float(gold_action_dict['level_total_cost_%s' % _lv]) / float(cost_user_num), 2)
            gold_action_dict.pop(level_cost_key)
    # 计算到达人数
    for _lv in xrange(1, 121):
        gold_action_dict['level_user_arrive_%s' % _lv] = _get_arrive_level_num(_lv)

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'USER_GOLD_CONSUME', 'w')
    pickle.dump(gold_action_dict, out_put_file)
    out_put_file.close()

def _output_USER_STONE_CONSUME(split_date):
    """
        输出用户钻石消耗部分数据
    """
    print("USER_STONE_CONSUME")
    # 计算等级消耗表数据
    for _lv in xrange(1, 121):
        level_cost_key = 'level_user_cost_set_%s' % _lv
        if level_cost_key in stone_action_dict:
            cost_user_num = len(stone_action_dict[level_cost_key])
            stone_action_dict['level_user_cost_num_%s' % _lv] = cost_user_num
            stone_action_dict['level_arppu_%s' % _lv] = round(float(stone_action_dict['level_total_cost_%s' % _lv]) / float(cost_user_num), 2)
            stone_action_dict.pop(level_cost_key)
    # 计算到达人数
    for _lv in xrange(1, 121):
        stone_action_dict['level_user_arrive_%s' % _lv] = _get_arrive_level_num(_lv)


    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'USER_STONE_CONSUME', 'w')
    pickle.dump(stone_action_dict, out_put_file)

    out_put_file.close()

def _output_USER_GENERATE_GOLD(split_date):
    """
        用户金币产出
    """
    print("USER_GENERATE_GOLD")
    total_generate = gold_action_dict['total_add']
    total_cost =  gold_action_dict['total_cost']
    generate_actions = gold_action_dict.get("add_gold_actions_set", set())
    result = dict()
    result['total_generate'] = total_generate
    result['total_cost'] = total_cost
    result['actions'] = generate_actions

    for _action in generate_actions:
        _action_generate = gold_action_dict[_action]
        result[_action] = _action_generate

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'USER_GENERATE_GOLD', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

def _output_USER_GENERATE_STONE(split_date):
    """
        用户钻石产出
    """
    print("USER_GENERATE_STONE")
    total_generate = stone_action_dict['total_add']
    total_cost =  stone_action_dict['total_cost']
    generate_actions = stone_action_dict.get("add_stone_actions_set", set())
    result = dict()
    result['total_generate'] = total_generate
    result['total_cost'] = total_cost
    result['actions'] = generate_actions

    for _action in generate_actions:
        _action_generate = stone_action_dict[_action]
        result[_action] = _action_generate

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'USER_GENERATE_STONE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

def _output_USER_COST_STONE(split_date):
    """
        用户钻石消耗
    """
    print("USER_COST_STONE")
    total_generate = stone_action_dict['total_add']
    total_cost =  stone_action_dict['total_cost']
    generate_actions = stone_action_dict.get("cost_stone_actions_set", set())
    result = dict()
    result['total_generate'] = total_generate
    result['total_cost'] = total_cost
    result['actions'] = generate_actions

    for _action in generate_actions:
        _action_generate = stone_action_dict[_action]
        result[_action] = _action_generate

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'USER_COST_STONE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

def _output_USER_COST_GOLD(split_date):
    """
        金币消耗
    """
    print("USER_COST_GOLD")
    total_generate = gold_action_dict['total_add']
    total_cost =  gold_action_dict['total_cost']
    generate_actions = gold_action_dict.get("cost_gold_actions_set", set())
    result = dict()
    result['total_generate'] = total_generate
    result['total_cost'] = total_cost
    result['actions'] = generate_actions

    for _action in generate_actions:
        _action_generate = gold_action_dict[_action]
        result[_action] = _action_generate

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'USER_COST_GOLD', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


# -------------------------------------------------消费点分析------------------------------------------------------
def _output_DAILY_CONSUME_DISTRIBUTED_STONE(split_date):
    """
        日常钻石消费点分析
        事件	钻石数	人数	次数	参与率	钻石消耗占比	人数占比
    """
    print("DAILY_CONSUME_DISTRIBUTED_STONE")
    # 所有消耗事件
    generate_actions = stone_action_dict.get("cost_stone_actions_set", set())
    total_stone = stone_action_dict.get("total_cost", 0)
    result = dict()
    result['actions'] = generate_actions
    total_user = 0
    for _action in generate_actions:
        _action_generate = stone_action_dict[_action]
        # 事件 - UID
        key_action_user_uid = "action_%s_user_set" % _action
        user_num = len(stone_action_dict[key_action_user_uid])
        total_user += user_num
        # 事件 - 日志次数
        key_action_log_count = "action_%s_log_count" % _action
        log_num = stone_action_dict[key_action_log_count]

        result['action_%s_stone' % _action] = _action_generate
        result['action_%s_user_num' % _action] = user_num
        result['action_%s_log_num'% _action] = log_num
        result['action_%s_stone_rate'% _action] = round(float(_action_generate)/float(total_stone), 2)

    for _action in generate_actions:
        result['action_%s_user_rate' % _action] = round(float(result['action_%s_user_num' % _action])/float(total_user), 2)

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'DAILY_CONSUME_DISTRIBUTED_STONE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_DAILY_CONSUME_DISTRIBUTED_GOLD(split_date):
    """
        日常金币消费点分析
        事件	金币数	人数	次数	参与率	金币消耗占比	人数占比
    """
    print("DAILY_CONSUME_DISTRIBUTED_GOLD")
    # 所有消耗事件
    generate_actions = gold_action_dict.get("cost_gold_actions_set", set())
    total_gold = gold_action_dict.get("total_cost", 0)
    result = dict()
    result['actions'] = generate_actions
    total_user = 0
    for _action in generate_actions:
        _action_generate = gold_action_dict[_action]

        # 事件 - UID
        key_action_user_uid = "action_%s_user_set" % _action
        user_num = len(gold_action_dict[key_action_user_uid])
        total_user += user_num
        # 事件 - 日志次数
        key_action_log_count = "action_%s_log_count" % _action
        log_num = gold_action_dict[key_action_log_count]

        result['action_%s_gold' % _action] = _action_generate
        result['action_%s_user_num' % _action] = user_num
        result['action_%s_log_num'% _action] = log_num
        result['action_%s_gold_rate'% _action] = round(float(_action_generate)/float(total_gold), 2)

    for _action in generate_actions:
        result['action_%s_user_rate' % _action] = round(float(result['action_%s_user_num' % _action])/float(total_user), 2)

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'DAILY_CONSUME_DISTRIBUTED_GOLD', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

def _output_USER_HOLD_GOLD(split_date):
    """
         玩家持有金币数
    """
    print("USER_HOLD_GOLD")
    global user_active_num
    total_gold = sum([_val['cur_gold'] for _val in user_cur_gold_dict.values()])
    total_user = len(user_cur_gold_dict.keys())

    _dat = dict()
    _dat['total_gold'] = total_gold
    _dat['total_user'] = total_user
    _dat['active_user'] = user_active_num

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'USER_HOLD_GOLD', 'w')
    pickle.dump(_dat, out_put_file)
    out_put_file.close()


def _output_USER_HOLD_STONE(split_date):
    """
        玩家持有钻石数
    """
    print("USER_HOLD_STONE")
    total_stone = sum([_val['cur_stone'] for _val in user_cur_stone_dict.values()])
    total_user = len(user_cur_stone_dict.keys())
    global user_active_num

    _dat = dict()
    _dat['total_stone'] = total_stone
    _dat['total_user'] = total_user
    _dat['active_user'] = user_active_num

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'USER_HOLD_STONE', 'w')
    pickle.dump(_dat, out_put_file)
    print(_dat)
    out_put_file.close()


def _output_USER_COST_GOLD_WITH_VIP(split_date):
    """
        VIP消耗金币数
    """
    print("USER_COST_GOLD_WITH_VIP")
    # 所有消耗金币的action
    generate_actions = gold_action_dict.get("cost_gold_actions_set", set())

    vip_0_total = 0
    vip_0_user = 0
    vip_0_count = 0
    vip_other_total = 0
    vip_other_user = 0
    vip_other_count = 0
    result = []
    for _action in generate_actions:
        _dat = dict()
        _dat['action'] = _action
        for _vip in xrange(0, 13):
            vip_cost_key = 'vip%s_%s_total' % (_vip, _action)
            vip_user_key = 'vip%s_%s_user_set' % (_vip, _action)
            key_vip_count = 'vip%s_%s_count' % (_vip, _action)
            _vip_user_num = len(gold_action_dict.get(vip_user_key, set()))
            _vip_total_cost = gold_action_dict.get(vip_cost_key, 0)
            _vip_log_count = gold_action_dict.get(key_vip_count, 0)
            _dat['vip_%s_cost_gold_num' % _vip] = _vip_total_cost
            _dat['vip_%s_cost_gold_user_num' % _vip] = _vip_user_num
            if _vip:
                vip_other_total += _vip_total_cost
                vip_other_user += _vip_user_num
                vip_other_count += _vip_log_count
            else:
                vip_0_total += _vip_total_cost
                vip_0_user += _vip_user_num
                vip_0_count += _vip_log_count
            # 插入结果数据
        _dat['recharge_user_num'] = vip_other_user
        _dat['recharge_user_log_num'] = vip_other_count
        _dat['vip0_user_num'] = vip_0_user
        _dat['vip0_user_log_num'] = vip_0_count
        _dat['total_cost_gold_num'] = vip_0_total + vip_other_total
        result.append(_dat)


    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'USER_COST_GOLD_WITH_VIP', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()

def _output_USER_COST_STONE_WITH_VIP(split_date):
    """
        VIP消耗金币数
    """
    print("USER_COST_STONE_WITH_VIP")
    # 所有消耗金币的action
    generate_actions = stone_action_dict.get("cost_stone_actions_set", set())

    vip_0_total = 0
    vip_0_user = 0
    vip_0_count = 0
    vip_other_total = 0
    vip_other_user = 0
    vip_other_count = 0
    result = []
    for _action in generate_actions:
        _dat = dict()
        _dat['action'] = _action
        for _vip in xrange(0, 13):
            vip_cost_key = 'vip%s_%s_total' % (_vip, _action)
            vip_user_key = 'vip%s_%s_user_set' % (_vip, _action)
            key_vip_count = 'vip%s_%s_count' % (_vip, _action)
            _vip_user_num = len(stone_action_dict.get(vip_user_key, set()))
            _vip_total_cost = stone_action_dict.get(vip_cost_key, 0)
            _vip_log_count = stone_action_dict.get(key_vip_count, 0)
            _dat['vip_%s_cost_stone_num' % _vip] = _vip_total_cost
            _dat['vip_%s_cost_stone_user_num' % _vip] = _vip_user_num
            if _vip:
                vip_other_total += _vip_total_cost
                vip_other_user += _vip_user_num
                vip_other_count += _vip_log_count
            else:
                vip_0_total += _vip_total_cost
                vip_0_user += _vip_user_num
                vip_0_count += _vip_log_count
            # 插入结果数据
        _dat['recharge_user_num'] = vip_other_user
        _dat['recharge_user_log_num'] = vip_other_count
        _dat['vip0_user_num'] = vip_0_user
        _dat['vip0_user_log_num'] = vip_0_count
        _dat['total_cost_stone_num'] = vip_0_total + vip_other_total
        result.append(_dat)

    out_put_file_path = OUT_PUT_PATH + str(split_date) + "/"
    out_put_file = open(out_put_file_path + 'USER_COST_STONE_WITH_VIP', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _insert_gold_action(log_dict):
    """
        统计金币事件
    """
    global gold_action_dict
    action = log_dict['action']
    add_gold = log_dict.get('add_gold', 0)
    cost_gold = log_dict.get('cost_gold', 0)

    # 消耗和产出
    if add_gold + cost_gold:
        gold_action_dict['total_cost'] += cost_gold
        gold_action_dict['total_add'] += add_gold
        # 事件部分
        if cost_gold:
            _cost_actions_set = gold_action_dict.get("cost_gold_actions_set", set())
            _cost_actions_set.add(action)
            gold_action_dict["cost_gold_actions_set"] = _cost_actions_set
        if add_gold:
            _add_gold_actions_set = gold_action_dict.get("add_gold_actions_set", set())
            _add_gold_actions_set.add(action)
            gold_action_dict["add_gold_actions_set"] = _add_gold_actions_set

        gold_action_dict[action] = gold_action_dict.get(action, 0) + add_gold - cost_gold
        # 事件 - UID
        key_action_user_uid = "action_%s_user_set" % action
        action_user_uid_set = gold_action_dict.get(key_action_user_uid, set())
        action_user_uid_set.add(log_dict['uid'])
        gold_action_dict[key_action_user_uid] = action_user_uid_set
        # 事件 - 日志次数
        key_action_log_count = "action_%s_log_count" % action
        gold_action_dict[key_action_log_count] = gold_action_dict.get(key_action_log_count, 0) + 1

        # vip 部分
        vip_key = 'vip%s_%s_total' % (log_dict['vip_level'], action)
        gold_action_dict[vip_key] = gold_action_dict.get(vip_key, 0) + add_gold - cost_gold
        key_vip_count = 'vip%s_%s_count' % (log_dict['vip_level'], action)
        gold_action_dict[key_vip_count] = gold_action_dict.get(key_vip_count, 0) + 1

        vip_key = 'vip%s_%s_user_set' % (log_dict['vip_level'], action)
        user_uid_set = gold_action_dict.get(vip_key, set())
        user_uid_set.add(log_dict['uid'])
        gold_action_dict[vip_key] = user_uid_set


    # 等级消耗数量
    if cost_gold:
        level_key = 'level_total_cost_%s' % log_dict['level']
        gold_action_dict[level_key] = gold_action_dict.get(level_key, 0) + cost_gold
        # 等级消耗人数
        level_cost_key = 'level_user_cost_set_%s' % log_dict['level']
        level_cost_user_uid_set = gold_action_dict.get(level_cost_key, set())
        level_cost_user_uid_set.add(log_dict['uid'])
        gold_action_dict[level_cost_key] = level_cost_user_uid_set


        # 首次消耗增加部分
        if log_dict['total_cost_gold'] - 22000 == log_dict['cost_gold']:

            key_first_cost_total_gold = 'first_total_cost'
            gold_action_dict[key_first_cost_total_gold] = gold_action_dict.get(key_first_cost_total_gold, 0) + cost_gold
            # 首次消耗人uid_action
            key_first_cost_user_set = 'first_cost_user_set_%s' % log_dict['action']
            first_cost_user_uid_set = gold_action_dict.get(key_first_cost_user_set, set())
            first_cost_user_uid_set.add(log_dict['uid'])
            gold_action_dict[key_first_cost_user_set] = first_cost_user_uid_set
            # 插入事件列表
            key_first_cost_action_set = 'first_cost_action_set'
            first_cost_action_set = gold_action_dict.get(key_first_cost_action_set, set())
            first_cost_action_set.add(log_dict['action'])
            gold_action_dict[key_first_cost_action_set] = first_cost_action_set
            # 事件消耗数值
            gold_action_dict['first_cost_%s' % action] = gold_action_dict.get('first_cost_%s' % action, 0) + cost_gold


def _insert_stone_action(log_dict):
    """
        统计金币事件
    """
    global stone_action_dict
    action = log_dict['action']
    add_stone = log_dict.get('add_stone', 0)
    cost_stone = log_dict.get('cost_stone', 0)
    if add_stone + cost_stone:
        stone_action_dict['total_cost'] += cost_stone
        stone_action_dict['total_add'] += add_stone
        # 事件部分
        if cost_stone:
            _cost_actions_set = stone_action_dict.get("cost_stone_actions_set", set())
            _cost_actions_set.add(action)
            stone_action_dict["cost_stone_actions_set"] = _cost_actions_set
        if add_stone:
            _add_actions_set = stone_action_dict.get("add_stone_actions_set", set())
            _add_actions_set.add(action)
            stone_action_dict["add_stone_actions_set"] = _add_actions_set
        stone_action_dict[action] = stone_action_dict.get(action, 0) + add_stone - cost_stone

        # 事件 - UID
        key_action_user_uid = "action_%s_user_set" % action
        action_user_uid_set = stone_action_dict.get(key_action_user_uid, set())
        action_user_uid_set.add(log_dict['uid'])
        stone_action_dict[key_action_user_uid] = action_user_uid_set
        # 事件 - 日志次数
        key_action_log_count = "action_%s_log_count" % action
        stone_action_dict[key_action_log_count] = stone_action_dict.get(key_action_log_count, 0) + 1

        # vip 部分
        vip_key = 'vip%s_%s_total' % (log_dict['vip_level'], action)
        stone_action_dict[vip_key] = stone_action_dict.get(vip_key, 0) + add_stone - cost_stone
        key_vip_count = 'vip%s_%s_count' % (log_dict['vip_level'], action)
        stone_action_dict[key_vip_count] = stone_action_dict.get(key_vip_count, 0) + 1

        vip_key = 'vip%s_%s_user_set' % (log_dict['vip_level'], action)
        user_uid_set = stone_action_dict.get(vip_key, set())
        user_uid_set.add(log_dict['uid'])
        stone_action_dict[vip_key] = user_uid_set

    # 等级消耗数量
    if cost_stone:
        level_key = 'level_total_cost_%s' % log_dict['level']
        stone_action_dict[level_key] = stone_action_dict.get(level_key, 0) + cost_stone
        # 等级消耗人数
        level_cost_key = 'level_user_cost_set_%s' % log_dict['level']
        level_cost_user_uid_set = stone_action_dict.get(level_cost_key, set())
        level_cost_user_uid_set.add(log_dict['uid'])
        stone_action_dict[level_cost_key] = level_cost_user_uid_set

        # 首次消耗增加部分
        if log_dict['total_cost_stone'] == log_dict['cost_stone']:
            key_first_cost_total_stone = 'first_total_cost'
            stone_action_dict[key_first_cost_total_stone] = stone_action_dict.get(key_first_cost_total_stone, 0) + cost_stone
            # 首次消耗人uid_action
            key_first_cost_user_set = 'first_cost_user_set_%s' % log_dict['action']
            first_cost_user_uid_set = stone_action_dict.get(key_first_cost_user_set, set())
            first_cost_user_uid_set.add(log_dict['uid'])
            stone_action_dict[key_first_cost_user_set] = first_cost_user_uid_set
            # 插入事件列表
            key_first_cost_action_set = 'first_cost_action_set'
            first_cost_action_set = stone_action_dict.get(key_first_cost_action_set, set())
            first_cost_action_set.add(log_dict['action'])
            stone_action_dict[key_first_cost_action_set] = first_cost_action_set
            # 事件消耗数值
            stone_action_dict['first_cost_%s' % action] = stone_action_dict.get('first_cost_%s' % action, 0) + cost_stone


def _insert_treasure_frag(uid, log_time, channel_id, server_id, action, level, item_action,  treasure_frag_lst):
    """
        插入宝物碎片数据
    """
    if treasure_frag_lst:
        treasure_frag_lst = map(int, treasure_frag_lst)
        result = []
        for index in xrange(0, len(treasure_frag_lst), 2):
            _tid = treasure_frag_lst[index]
            if item_action == TREASURE_FRAGMENT_ACTION_LST[0]:
                _num = treasure_frag_lst[index + 1]
            else:
                _num = -treasure_frag_lst[index + 1]

            result.append({"uid": uid, "log_time": log_time, "channel_id":channel_id, "server_id":server_id, "action":action,"level":level, "tid":_tid, "num":_num})
        return result
    return None

def _insert_treasure(uid, log_time, channel_id, server_id, action, level, item_action,  treasure_lst):
    """
        插入宝物碎片数据
    """
    if treasure_lst:
        treasure_lst = map(int, treasure_lst)
        result = []
        for index in xrange(0, len(treasure_lst), 2):
            _tid = treasure_lst[index]
            if item_action == TREASURE_ACTION_LST[0]:
                _num = treasure_lst[index + 1]
            else:
                if index + 1 < len(treasure_lst):
                    _num = -treasure_lst[index + 1]
                else:
                    _num = -1

            result.append({"uid": uid, "log_time": log_time, "channel_id":channel_id, "server_id":server_id, "action":action, "level":level, "tid":_tid, "num":_num})
        return result
    return None

def _insert_user_team(uid, log_time, channel_id, server_id, team_lst):
    """
        插入玩家队伍信息
    """
    if team_lst:
        team_lst = map(int, team_lst)
        team_monster_num = len(team_lst) / 3
        monster_team_key = ""
        dat = {"uid": uid, "log_time": log_time, "channel_id":channel_id, "server_id":server_id}
        for index in range(0, team_monster_num):
            _num = index + 1
            monster_team_key += ",monster_%s,star_%s,level_%s" % (_num, _num, _num)
            dat.update({
                "monster_%s" % _num : team_lst[index * 3],
                "star_%s" % _num : team_lst[index * 3 + 1],
                "level_%s" % _num : team_lst[index * 3 + 2]
            })
        return [dat]
    return None

def _insert_item_change_log(uid, log_time, channel_id, server_id, action, level, item_action,  item_lst):
    """
        插入物品改变
        # 时间 物品ID 物品数量 用户ID 事件
    """
    if item_lst:
        item_lst = map(int, item_lst)
        result = []
        for index in xrange(0, len(item_lst), 2):
            _tid = item_lst[index]
            if item_action == ITEM_ACTION_LST[0]:
                _num = item_lst[index + 1]
            else:
                _num = -item_lst[index + 1]
            result.append({"uid": uid, "log_time": log_time, "channel_id":channel_id, "server_id":server_id, "action":action, "level": level, "tid":_tid, "num":_num})
        return result
    return None

def _insert_equip_change_log(uid, log_time, channel_id, server_id, action, level, item_action,  equip_lst):
    """
        插入物品改变
        # 时间 物品ID 物品数量 用户ID 事件
    """
    if equip_lst:
        equip_lst = map(int, equip_lst)
        result = []
        for index in xrange(0, len(equip_lst), 2):
            _tid = equip_lst[index]
            if item_action == EQUIP_ACTION_LST[0]:
                _num = equip_lst[index + 1]
            else:
                _num = -equip_lst[index + 1]

            result.append({"uid": uid, "log_time": log_time, "channel_id":channel_id, "server_id":server_id, "action":action, "level": level, "tid":_tid, "num":_num})
        return result
    return None

def _insert_monster_change_log(uid, log_time, channel_id, server_id, action, level, item_action,  monster_lst):
    """
        插入物品改变
        # 时间 物品ID 物品数量 用户ID 事件
    """
    if monster_lst:
        monster_lst = map(int, monster_lst)
        result = []
        for index in xrange(0, len(monster_lst), 3):
            _tid = monster_lst[index]
            _star = monster_lst[index + 1]
            if item_action == MONSTER_ACTION_LST[0]:
                _num = monster_lst[index + 2]
            else:
                _num = -monster_lst[index + 2]
            result.append({"uid": uid, "log_time": log_time, "channel_id":channel_id, "server_id":server_id, "action":action, "level": level, "tid":_tid, "num":_num, "star": _star})
        return result
    return None


def _start_insert_to_mysql():
    """
        插入mysql
    """
    mysql_connect = mysql.Connection(CATCH_SQL_HOST, 'manager', 'root', CATCH_SQL_PAS)

    sleep_time = float(1) / float(500)

    while len(mysql_queue):
        queue_num = len(mysql_queue)
        # print("准备插入mysql当前队列长度 " + str(queue_num))
        _sql = ''
        for i in xrange(min(queue_num, 500)):
            _sql += mysql_queue.pop()
        if _sql:
            mysql_connect.execute(_sql)
        time.sleep(sleep_time)

if __name__ == "__main__":
    start(sys.argv)

# start(['2015-06-05', '2015-06-05'])>>>>>>> .r25559
