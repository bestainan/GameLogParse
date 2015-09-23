# -*- coding:utf-8 -*-


"""
    新手引导完成度（需要根据新手引导具体情况进行修订）
查询日期	20101101
分区查询	总/1区/2区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道标示	UC/91	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）


新手引导完成度	选取用户在新手引导中的每一步操作，新手引导机制需要与研发确认是否有记录请求

项目编号	项目名称	到达人数	完成人数	分步完成率	累积完成率
1	启动客户端
2	登入请求
3	创建角色请求
4	开场动画1
……	开场动画2
……
30
引导结束总计
PS：本表人数均取角色数

"""

from util import daily_log_dat
from util import game_define


def get_table(search_date, channel_id=-1, server_id=-1):

    new_log_lst = daily_log_dat.get_new_log_lst(search_date, search_date)
    if channel_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)

    #获取全部新手引导日志
    all_newbie_log_lst = daily_log_dat.filter_logs(new_log_lst, action=game_define.EVENT_ACTION_FINISH_NEWBIE)
    # 总共5个引导步骤 （1-6）
    total_user = daily_log_dat.get_set_num_with_key(all_newbie_log_lst, 'uid')
    complete_user_dict = dict()
    newbie_name = [u'第一场战斗', u'抽取宝贝球', u'加入队伍', u'自动战斗', u'每日任务']

    for i in xrange(1, 6):
        # 当前引导的所有日志
        guide_index_log_lst = daily_log_dat.filter_logs(all_newbie_log_lst, function=lambda x: x['newbie_id'] == i)
        complete_user_num = daily_log_dat.get_set_num_with_key(guide_index_log_lst, 'uid')
        complete_user_dict[i] = complete_user_num

    table_result = []
    for i in xrange(1, 6):
        next_num = complete_user_dict.get(i+1,0)
        row = [
            i,
            newbie_name[i-1],
            complete_user_dict[i], # 完成人数
        ]
        table_result.append(row)

    return table_result


# 获取比率
def _get_next_num_rate(next_num, complete_user_dict_i):
    """

    """
    if complete_user_dict_i <= 0:
        return 0
    return round(float(next_num) / float(complete_user_dict_i), 2)


# 获取比率
def _get_complete_user_dict_rate(complete_user_dict_i, total_user):
    """

    """
    if total_user <= 0:
        return 0
    return round(float(complete_user_dict_i) / float(total_user), 2)





