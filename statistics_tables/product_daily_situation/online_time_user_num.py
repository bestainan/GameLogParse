# -*- coding:utf-8 -*-

"""
用户在线数据
查询日期	20101101
分区查询	总/1区/2区	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
渠道标示	UC/91	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）


时间	与研发确认是否可以在服务器上写入这个数据保存，来计算在线人数，时间间隔由cp决定

2分钟（筛选2分钟，5分钟，10分钟）
2013/11/20 00:02:00	100
2013/11/20 00:04:00	100
2013/11/20 00:06:00	100
2013/11/20 00:08:00	100
2013/11/20 00:10:00	100
2013/11/20 00:12:00	100
2013/11/20 00:14:00	100
2013/11/20 00:16:00	100
2013/11/20 00:18:00	100
2013/11/20 00:20:00	100
2013/11/20 00:22:00	100
2013/11/20 00:24:00	100
2013/11/20 00:26:00	100

"""
import datetime
from util import daily_log_dat


def get_table(from_date, to_date, channel_id=-1, server_id=-1):
    """
        获取在线表数据
    """
    dis_minute = 5  # 5分钟间隔

    from_datetime = datetime.datetime.strptime(str(from_date), '%Y-%m-%d')
    to_datetime = datetime.datetime.strptime(str(to_date), '%Y-%m-%d')

    new_log_lst = daily_log_dat.get_new_log_lst(from_datetime.date(), to_datetime.date())

    if channel_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['platform_id'] == channel_id)
    if server_id >= 0:
        new_log_lst = daily_log_dat.filter_logs(new_log_lst, function=lambda x: x['server_id'] == server_id)

    total_line = int((to_datetime - from_datetime).total_seconds() / (dis_minute * 60))

    row_lst = []
    for line in xrange(total_line):
        row = []
        get_start_datetime = from_datetime + datetime.timedelta(minutes=dis_minute * line)
        get_end_datetime = get_start_datetime + datetime.timedelta(minutes=dis_minute)

        cur_user_num = daily_log_dat.get_set_num_with_key(new_log_lst, 'uid', function=lambda log: get_start_datetime <= log['log_time'] <= get_end_datetime)
        row.append(get_end_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        row.append(cur_user_num)
        row_lst.append(row)
    return row_lst

