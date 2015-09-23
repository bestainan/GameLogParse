# -*- coding:utf-8 -*-
"""
    创建角色
"""
from action import action_base
from util import game_define


def log(user, monster_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_CREATE_ROLE
    name = user.player.name.decode('utf8').encode('gb2312')
    role_id = str(user.player.role_id)

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(name)
    log_lst.append(str(role_id))
    log_lst.append(str(monster_str))
    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['name'] = "test"
    result['role_id'] = log_part_lst[2]
    result['add_monster_list'] = action_base.get_val(log_part_lst, 3, [], True)
    return result