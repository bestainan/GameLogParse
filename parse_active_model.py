# -*- coding:utf-8 -*-

"""
    解析所有活动事件
"""
import os
import sys
import datetime
from catch_split_log.active_model import finger_guess
from catch_split_log.active_model import fishing
from catch_split_log.active_model import massage
from catch_split_log.active_model import question
from catch_split_log.active_model import tonic
from util.logs_out_in_path import LOG_PATH
from util.logs_out_path_of_parse import LOG_PATH
def start_parse(split_date):
    """
        获取并拆分一天的日志
    """
    err=open(LOG_PATH+"%s/%s"%("Error",split_date),'a+')
    nor=open(LOG_PATH+"%s/%s"%("Normal",split_date),'a+')
    sys.stdout=nor
    startime=datetime.datetime.now()
    print 'active_model解析开始',startime
    start_list = [finger_guess, fishing, massage, question, tonic]

    for func in start_list:
        try:
            sys.stdout=nor
            func.start(split_date)
        except Exception,e :
            sys.stdout=err
            print datetime.datetime.now(),str(func),"  Error:",e,"\n"
            pass
    sys.stdout=nor

    endtime=datetime.datetime.now()
    print 'active_model解析结束',endtime
    print 'active_model共花费时间',(endtime-startime).seconds ,'秒' ,'\n\n'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        split_date_str = sys.argv[1]
        split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
        start_parse(split_date)
    else:
        split_date = datetime.date.today() - datetime.timedelta(days=1)
        start_parse(split_date)
