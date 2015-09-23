# -*- coding:utf-8 -*-
"""
    添加礼包
"""
from game_manager.action_gm import action_base_gm
from util import game_define
import datetime


def log(manager, server_id,platform_id, endtime, name,  item_id1, item_num1, item_id2, item_num2, item_id3, item_num3, gold, stone):
    """
        输出日志
    """
    action = game_define.GM_ACTION_INSERT_GIFT
    log_lst = action_base_gm.log_base(manager)

    log_lst.append(str(action))
    log_lst.append(str(server_id))
    log_lst.append(str(platform_id))
    log_lst.append(endtime.strftime("%Y-%m-%d"))
    log_lst.append(name.encode('utf-8'))
    log_lst.append(str(item_id1))
    log_lst.append(str(item_num1))
    log_lst.append(str(item_id2))
    log_lst.append(str(item_num2))
    log_lst.append(str(item_id3))
    log_lst.append(str(item_num3))
    log_lst.append(str(gold))
    log_lst.append(str(stone))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['server_id'] = log_part_lst[1]
    result['platform_id'] = log_part_lst[2]
    result['endtime'] = log_part_lst[3]
    result['name'] = log_part_lst[4].decode('utf-8')
    result['item_id1'] = log_part_lst[5]
    result['item_num1'] = log_part_lst[6]
    result['item_id2'] = log_part_lst[7]
    result['item_num2'] = log_part_lst[8]
    result['item_id3'] = log_part_lst[9]
    result['item_num3'] = log_part_lst[10]
    result['gold'] = log_part_lst[11]
    result['stone'] = log_part_lst[12]

    return result
