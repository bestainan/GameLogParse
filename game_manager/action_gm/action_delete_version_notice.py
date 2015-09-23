# -*- coding:utf-8 -*-
"""
    删除版本公告
"""
from game_manager.action_gm import action_base_gm
from util import game_define


def log(manager, version):
    """
        输出日志
    """
    action = game_define.GM_ACTION_DELETE_VERSION_NOTICE
    log_lst = action_base_gm.log_base(manager)

    log_lst.append(str(action))
    log_lst.append(str(version))

    log_str = '$$'.join(log_lst)
    return log_str


def parse(log_part_lst):
    """
        解析
    """
    result = dict()
    result['action'] = int(log_part_lst[0])
    result['version'] = log_part_lst[1]

    return result
