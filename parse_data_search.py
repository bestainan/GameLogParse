# -*- coding:utf-8 -*-

"""
    解析所有联盟事件
"""
import os
import sys
import datetime

from catch_split_log.GM import user_cost,user_get,equipment_st
from util.logs_out_path_of_parse import LOG_PATH

def start_parse(split_date):
    """
        获取并拆分一天的日志
    """
    err=open(LOG_PATH+"%s/%s"%("Error",split_date),'a+')
    nor=open(LOG_PATH+"%s/%s"%("Normal",split_date),'a+')
    sys.stdout=nor
    startime=datetime.datetime.now()
    print 'data_search解析开始',startime
    start_list = [user_cost, user_get, equipment_st]  #

    for func in start_list:
        try:
            sys.stdout=nor
            func.start(split_date)
        except Exception,e :
            # sys.stdout=err
            print datetime.datetime.now(),str(func),"  Error:",e,"\n"
            pass
    sys.stdout=nor

    endtime=datetime.datetime.now()
    print 'data_search解析结束',endtime
    print 'data_search共花费时间',(endtime-startime).seconds,'秒' ,'\n\n'


if __name__ == '__main__':
    if sys.argv[1]:
        split_date = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        start_parse(split_date)
    else:
        split_date = datetime.date.today() - datetime.timedelta(days=1)
        start_parse(split_date)


