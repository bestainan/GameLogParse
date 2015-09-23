# -*- coding:utf-8 -*-
"""
    角色登陆
"""
import datetime

from action import action_base
from util import game_define


def log(user, account_id, account_name, dev_id, login_ip, login_distance_days, team_str):
    """
        输出日志
    """
    action = game_define.EVENT_ACTION_ROLE_LOGIN
    name = user.player.name
    # 月卡剩余天数
    month_card_days = 0
    month_card_deadline = user.player.month_50_indate
    now_date = datetime.date.today()
    if month_card_deadline and now_date < month_card_deadline:
        month_card_days = (month_card_deadline - now_date).days

    log_lst = action_base.log_base(user)

    log_lst.append(str(action))
    log_lst.append(name)
    log_lst.append(str(account_id))
    log_lst.append(str(account_name))
    log_lst.append(str(dev_id))
    log_lst.append(str(login_ip))
    log_lst.append(str(month_card_days))
    log_lst.append(str(login_distance_days))
    log_lst.append(str(team_str))
    log_str = '$$'.join(log_lst)
    return log_str

def parse(log_part_lst):
    """
        解析
    """

    result = dict()
    result['action'] = int(log_part_lst[0])
    result['player_name'] = log_part_lst[1].decode('utf8')
    result['account_id'] = log_part_lst[2]
    result['account_name'] = log_part_lst[3]
    result['dev_id'] = log_part_lst[4]
    result['login_ip'] = log_part_lst[5]
    result['month_card_days'] = int(log_part_lst[6])
    result['login_dis_days'] = int(log_part_lst[7])
    result['team_list'] = map(int, action_base.get_val(log_part_lst, 8, [], True))

    return result
