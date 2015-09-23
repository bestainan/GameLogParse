# -*- coding:utf-8 -*-

"""
    解析所有联盟事件
"""
import os
import sys
import datetime

from catch_split_log.active_union import union_count,union_buy_reward,union_shop,union_sign,union_stage,friend_count,union_detail
from util.logs_out_path_of_parse import LOG_PATH
def start_parse(split_date):
    """
        获取并拆分一天的日志
    """
    err = open(LOG_PATH+"%s/%s" % ("Error", split_date), 'a+')
    nor = open(LOG_PATH+"%s/%s" % ("Normal", split_date), 'a+')
    sys.stdout = nor
    startime = datetime.datetime.now()
    print 'union解析开始', startime, '\n\n'

    start_list = [union_sign, union_shop, union_buy_reward , union_stage, friend_count, union_detail,union_count]
    for func in start_list:
        try:
            sys.stdout = nor
            func.start(split_date)
        except Exception, e:
            sys.stdout = err
            print datetime.datetime.now(), str(func), "  Error:", e, "\n"
            pass
    sys.stdout = nor

    endtime = datetime.datetime.now()
    print 'union解析结束', endtime
    print 'union共花费时间',(endtime-startime).seconds, '秒', '\n\n'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        split_date_str = sys.argv[1]
        split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
        start_parse(split_date)
    else:
        split_date = datetime.date.today() - datetime.timedelta(days=1)
        start_parse(split_date)

