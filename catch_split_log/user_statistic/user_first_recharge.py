# -*- coding:utf-8 -*-

"""
玩家首冲情况
查询时间	开始时间	20100920	结束时间	20100923
渠道查询	所有渠道	（可以查单独的渠道，也可以查所有渠道，区服之间可进行多个同时选择）
分区查询	全服	（可以查单区，也可以查所有区，渠道之间可进行多个同时选择）
玩家最大等级		（最大等级为游戏设定英雄最大等级，后期等级变化后可调整）
玩家最小等级		（最小等级为1级）

注：首冲玩家数量表示每日新增首冲人数统计
日期	6月人数	30元人数	98元人数	198元人数	328元人数	488元人数	2000元人数
20101010
20101010
20101010
20101010
20101010
PS：本表人数均取角色数

"""
import datetime
import pickle
import sys
import os
import stat
from util import game_define
from mysql import mysql_connection
from util.logs_out_path_of_parse import get_parse_path


def start(split_date):
    """
        获取并拆分一天的日志
    """
    startime=datetime.datetime.now()
    print 'user_first_recharge解析开始',startime  ,'\n\n'
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST = get_parse_path(split_date)
    for _server_id in LOCAL_LOG_PATH_NAME_LST:
        try:
            out_put_file_path = OUT_PUT_PATH_LST[_server_id].format(cur_date=split_date, use_path="tables")
            if not os.path.exists(out_put_file_path):
                os.makedirs(out_put_file_path)
            os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

            start_time = datetime.datetime.now()
            print start_time

            # 玩家首冲情况
            _output_user_first_recharge(out_put_file_path, split_date, _server_id)

            end_time = datetime.datetime.now()
            print end_time
            print end_time-start_time
        except:
            pass
    endtime=datetime.datetime.now()
    print 'user_first_recharge解析结束',endtime
    print 'user_first_recharge共花费时间',(endtime-startime).seconds,'秒' ,'\n\n'


def _output_user_first_recharge(out_put_file_path, split_date, _server_id):
    print("USER_FIRST_RECHARGE")
    result = get_table(split_date, channel_id=-1, server_id=_server_id)

    out_put_file = open(out_put_file_path + 'USER_FIRST_RECHARGE', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def get_first_recharge_shop_index_uid_num(spe_column, row_date, specfy_column_name='shop_index', shop_index=-1, channel_id=-1, server_id=-1):
    """
        指定日期指定充值金额档充值人数
    """
    channel_server_str = ""
    if channel_id >= 0:
        channel_server_str += "platform_id = " + str(channel_id)+" and "
    if server_id >= 0:
        channel_server_str += " server_id = " + str(server_id)+" and "

    shop_index_str = ""
    if shop_index > 0:
        shop_index_str += " and  " + str(specfy_column_name) + " = " + str(shop_index)
    first_recharge_str = " and old_rmb = 0"

    connection = mysql_connection.get_log_mysql_connection_haima()
    # 获取次数
    sql = "SELECT count(%s) FROM EVENT_ACTION_RECHARGE_PLAYER where %s  action = %s and log_time >= '%s' and log_time < '%s' %s %s " % (spe_column, channel_server_str, game_define.EVENT_ACTION_RECHARGE_PLAYER, row_date, row_date + datetime.timedelta(days=1), shop_index_str, first_recharge_str)
    # print sql
    count = connection.query(sql)
    # print count
    return count[0].values()[0]


def get_table(search_date, channel_id=-1, server_id=-1):
    table_result = []
    row = []
    # 插入数据
    row.append(search_date.strftime('%Y-%m-%d'))
    # 充值档
    for shop_id in xrange(1, 9):
        user_num = get_first_recharge_shop_index_uid_num('uid', search_date, 'shop_index', shop_id, channel_id, server_id)
        # 插入数据
        row.append(user_num)
    table_result.append(row)

    return table_result




