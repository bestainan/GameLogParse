# -*- coding:utf-8 -*-
"""
    编辑运营活动
"""
from game_manager.action_gm import action_base_gm
from util import game_define


def log(manager, activity_id, server_id, begin_time, time_length, time_distance, is_forced_open, new, item_id1,
        item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone, free, exp, equip, monster, star, discount,
        title, detail, label, title2, label2, detail2):
    """
        输出日志
    """
    data = dict()
    action = game_define.GM_ACTION_CHANGE_ACTIVITY
    log_lst = action_base_gm.log_base(manager)
    data['activity_id'] = activity_id
    data['server_id'] = server_id
    data['begin_time'] = begin_time
    data['time_length'] = time_length
    data['time_distance'] = time_distance
    data['is_forced_open'] = is_forced_open
    data['new'] = new
    data['item_id1'] = item_id1
    data['item_num1'] = item_num1
    data['item_id2'] = item_id2
    data['item_num2'] = item_num2
    data['item_id3'] = item_id3
    data['item_num3'] = item_num3
    data['gold'] = gold
    data['stone'] = stone
    data['free'] = free
    data['exp'] = exp
    data['equip'] = equip
    data['monster'] = monster
    data['star'] = star
    data['discount'] = discount
    data['title'] = title
    data['detail'] = detail
    data['label'] = label
    data['title2'] = title2
    data['label2'] = label2
    data['detail2'] = detail2

    log_lst.append(str(action))
    log_lst.append(str(data))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['data'] = log_part_lst[1]

    return result
