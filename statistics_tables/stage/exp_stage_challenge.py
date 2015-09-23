# -*- coding:utf-8 -*-


"""
特殊副本通用表头
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

抓宠	参与人数	总参与次数	完成人数	总完成次数	到达要求人数	参与率	成功率
PS：挑战次数=角色挑战次数
"""

import datetime

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
        game_define.EVENT_ACTION_STAGE_EXP_WIN,
        game_define.EVENT_ACTION_STAGE_EXP_FAIL
    ]
    stage_action_log_lst = daily_log_dat.filter_logs(new_log_lst,
                                                     function=lambda log: log['action'] in stage_action_lst)
    table_lst = []
    search_days = (search_end_date - search_start_date).days+1
    for _day in xrange(search_days):
        row_date = search_start_date + datetime.timedelta(days=_day)
        # 获取当天的日志
        row_logs = daily_log_dat.filter_logs(stage_action_log_lst, function=lambda log:log['log_time'].date() == row_date)
        # 拆分日志
        catch_action_log_dict = daily_log_dat.split_log_action_logs(row_logs)
        # 获取可以参与人数
        all_user_num = daily_log_dat.get_set_num_with_key(new_log_lst, 'uid')
        # 获取实际参与人数
        join_user_num = daily_log_dat.get_set_num_with_key(row_logs, 'uid')
        # 参与次数
        join_num = len(row_logs)
        # 胜利日志
        win_logs = catch_action_log_dict.get(game_define.EVENT_ACTION_GET_CATCH_MONSTER_RESULT,[])
        win_user_num = daily_log_dat.get_set_num_with_key(win_logs, 'uid')
        #失败日志
        # fail_logs = []
        # 完成次数
        complete_count = len(win_logs)
        # 参与率
        join_rate = 0
        if all_user_num:
            join_rate = round(float(join_user_num)/float(all_user_num), 2)
        # 胜率
        win_rate = 0
        if join_num:
            win_rate = round(float(len(win_logs))/float(join_num), 2)

        row_lst = [
            row_date.strftime('%m/%d/%Y'),  # 日期
            join_user_num,  # 参与人数
            join_num, # 总参与次数
            win_user_num, # 完成人数
            complete_count, # 总完成次数
            all_user_num, # 到达要求人数
            join_rate, # 参与率
            win_rate # 成功率
        ]
        table_lst.append(row_lst)

    return table_lst

