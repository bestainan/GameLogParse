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
from util.logs_out_in_path import *
from util.logs_out_path_of_parse import get_parse_path

stone_action_dict = {
    'total_cost': 0,
    'total_add': 0
}
user_level_arrive_dict = dict()


def start(split_date):
    """
        获取并拆分一天的日志
    """
    # split_date = datetime.date.today() - datetime.timedelta(days=1)
    # split_date = datetime.datetime.strptime("2015-5-31", "%Y-%m-%d").date()
    # if len(args) > 1:
    #     try:
    #         split_date_str = args[1]
    #         split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
    #     except:
    #         sys.stderr.write("Err: Use daily_catch_split_log %Y-%m-%d")
    #         sys.exit(1)
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST = get_parse_path(split_date)
    # 本地打开
    for _server_id in LOCAL_LOG_PATH_NAME_LST:
        try:
            read_file = LOCAL_LOG_PATH_NAME_LST[_server_id].format(cur_date=split_date)
            log_lines = open(read_file, 'r')
            print(split_date)

            if log_lines:
                global user_level_arrive_dict, stone_action_dict
                user_level_arrive_dict = {}
                stone_action_dict = {'total_cost': 0, 'total_add': 0}
                for _log_line in log_lines:
                    _log_line = _log_line.strip()

                    log_dict = log_parse(_log_line)
                    if not log_dict:
                        continue

                    # 计算玩家等级分布
                    _insert_user_level_arrive_dict(log_dict)
                    # 计算钻石消耗产出
                    _insert_stone_action(log_dict)

                out_put_file_path = OUT_PUT_PATH_LST[_server_id].format(cur_date=split_date, use_path="tables")
                if not os.path.exists(out_put_file_path):
                    os.makedirs(out_put_file_path)
                os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

                # 玩家首次钻石消耗
                _output_USER_FIRST_STONE_CONSUME(out_put_file_path)
                time.sleep(0.1)

                # 日常钻石消费点分析
                _output_DAILY_CONSUME_DISTRIBUTED_STONE(out_put_file_path)
                time.sleep(0.1)

                # 玩家等级钻石消耗
                _output_USER_STONE_CONSUME(out_put_file_path)
                time.sleep(0.1)

                # 玩家钻石产出
                _output_USER_GENERATE_STONE(out_put_file_path)
                time.sleep(0.1)

                # 玩家钻石消耗
                _output_USER_COST_STONE(out_put_file_path)
                time.sleep(0.1)

                # 玩家vip 钻石消耗
                _output_USER_COST_STONE_WITH_VIP(out_put_file_path)
                time.sleep(0.1)
        except:
            pass


def _insert_user_level_arrive_dict(log_dict):
    """
        计算玩家等级分布
    """
    user_uid = log_dict['uid']
    global user_level_arrive_dict
    if user_uid in user_level_arrive_dict:
        save_level = user_level_arrive_dict[user_uid]
        if log_dict['level'] > save_level:
            user_level_arrive_dict[user_uid] = log_dict['level']
    else:
        user_level_arrive_dict[user_uid] = log_dict['level']


def _get_arrive_level_num(_lv):
    """
         获取玩家到达等级数
    """
    return len([user_lv for user_lv in user_level_arrive_dict.values() if user_lv >= _lv])


def _insert_stone_action(log_dict):
    """
        统计钻石事件
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

        try:
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
        except:
            pass

# -------------------------------------------------消费点分析------------------------------------------------------
def _output_USER_FIRST_STONE_CONSUME(out_put_file_path):
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
    out_put_file = open(out_put_file_path + 'USER_FIRST_STONE_CONSUME', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_DAILY_CONSUME_DISTRIBUTED_STONE(out_put_file_path):
    """
        日常钻石消费点分析
        事件	钻石数	人数	次数	参与率	钻石消耗占比	人数占比
    """
    print("DAILY_CONSUME_DISTRIBUTED_STONE")
    global stone_action_dict
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

    out_put_file = open(out_put_file_path + 'DAILY_CONSUME_DISTRIBUTED_STONE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_USER_STONE_CONSUME(out_put_file_path):
    """
        输出用户等级钻石消耗部分数据
    """
    print("USER_LEVEL_STONE_CONSUME")
    global stone_action_dict
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

    out_put_file = open(out_put_file_path + 'USER_STONE_CONSUME', 'w')
    pickle.dump(stone_action_dict, out_put_file)

    out_put_file.close()


# -------------------------------------------------数值平衡------------------------------------------------------
def _output_USER_GENERATE_STONE(out_put_file_path):
    """
        用户钻石产出
    """
    print("USER_GENERATE_STONE")
    total_generate = stone_action_dict['total_add']
    total_cost = stone_action_dict['total_cost']
    generate_actions = stone_action_dict.get("add_stone_actions_set", set())
    result = dict()
    result['total_generate'] = total_generate
    result['total_cost'] = total_cost
    result['actions'] = generate_actions

    for _action in generate_actions:
        _action_generate = stone_action_dict[_action]
        result[_action] = _action_generate

    out_put_file = open(out_put_file_path + 'USER_GENERATE_STONE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_USER_COST_STONE(out_put_file_path):
    """
        用户钻石消耗
    """
    print("USER_COST_STONE")
    total_generate = stone_action_dict['total_add']
    total_cost = stone_action_dict['total_cost']
    generate_actions = stone_action_dict.get("cost_stone_actions_set", set())
    result = dict()
    result['total_generate'] = total_generate
    result['total_cost'] = total_cost
    result['actions'] = generate_actions

    for _action in generate_actions:
        _action_generate = stone_action_dict[_action]
        result[_action] = _action_generate

    out_put_file = open(out_put_file_path + 'USER_COST_STONE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def _output_USER_COST_STONE_WITH_VIP(out_put_file_path):
    """
        VIP消耗钻石数
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

    out_put_file = open(out_put_file_path + 'USER_COST_STONE_WITH_VIP', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()