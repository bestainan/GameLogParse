# -*- coding:utf-8 -*-


"""
副本通用表头
注册时间	开始时间	20100919	结束时间	20100920
查询时间	开始时间	20100920	结束时间	20100923
游戏分区	总区服/一区/二区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道名称	所有	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）

挑战数	挑战这个副本的次数，以成功扣除体力为准
通过数	通过这个副本的次数
扫荡次数	钻石扫荡次数
成功率	通过数/挑战数
数据采集	选取2月份版本跟新首日用户数据进行分析


普通副本挑战次数，成功率

普通副本	副本名称	挑战数	通过数	扫荡次数	成功率	首次挑战次数	首次挑战成功次数
PS：挑战次数=角色挑战次数
"""

from util import daily_log_dat

from util import game_define


def get_table(search_start_date, search_end_date, register_start_date=None, register_end_date=None, channel_id=-1, server_id=-1):
    """
        获取展示表格
        register_start_date 注册开始时间
        register_end_date 注册结束时间
        search_start_date 查询开始时间
        search_end_date 查询结束时间
    """
    # 获取搜索区间日志
    new_log_lst = daily_log_dat.get_new_log_lst(search_start_date, search_end_date)

    if channel_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)
    #获取符合条件的日志
    if register_start_date and register_end_date:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda log: register_start_date <= log['install'] <= register_end_date)

    # 截取日志到 副本事件
    stage_action_lst = [
        game_define.EVENT_ACTION_TREASURE_BATTLE_WIN,
        game_define.EVENT_ACTION_TREASURE_BATTLE_FAIL
    ]

    stage_action_log_lst = daily_log_dat.filter_logs(new_log_lst,
                                                     function=lambda log: log['action'] in stage_action_lst)
    #根据action 拆分日志
    stage_action_log_dict = daily_log_dat.split_log_with_key_value(stage_action_log_lst, 'stage_index')

    # 遍历所有的关卡日志
    type_name_lst = [u'普通副本',u'精英副本',u'英雄副本',u'经验副本',u'金币副本',u'抓宠副本',u'世界BOSS副本',u'修行',u'夺宝']
    table_lst = []
    for _stage_index, _logs in stage_action_log_dict.items():
        #拆分日志 - 胜利部分
        _win_logs = daily_log_dat.filter_logs(_logs, action=game_define.EVENT_ACTION_STAGE_BATTLE_WIN)
        #拆分日志 - 失败部分
        _fail_logs = daily_log_dat.filter_logs(_logs, action=game_define.EVENT_ACTION_STAGE_BATTLE_FAIL)
        #拆分日志 - 扫荡部分
        # _mop_logs = daily_log_dat.filter_logs(_logs, action=game_define.EVENT_ACTION_STAGE_MOP)
        # 副本难度

        # 副本名称
        stage_name = '11'
        # 副本类型
        stage_type_name = type_name_lst[1]
        # 挑战次数
        challenge_num = len(_logs)
        # 通过次数
        win_num = len(_win_logs)
        # 扫荡次数
        # mop_num = len(_mop_logs)
        # 成功率
        win_rate = 0
        if challenge_num:
            win_rate = round(float(win_num)/float(challenge_num),2)
        # 首次挑战次数
        first_challenge_num = 0
        #首次挑战成功次数
        first_challenge_win = 0

        # 普通类型	副本名称	挑战数	通过数	扫荡次数	成功率	首次挑战次数	首次挑战成功次数
        row_lst = [stage_type_name, stage_name, challenge_num, win_num,  win_rate, first_challenge_num, first_challenge_win]
        table_lst.append(row_lst)
    if len(table_lst) > 0:
     print (str(table_lst[0]) +"treasure lens is ::"+ str(len(table_lst)))
    return table_lst












