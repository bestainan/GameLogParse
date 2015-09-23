# -*- coding:utf-8 -*-

"""
    解析所有关卡事件
"""
import os
import sys
import datetime
from catch_split_log.activity import friendly_shop
from catch_split_log.activity import give_me_give_you
from catch_split_log.activity import max_will
from catch_split_log.activity import wei_chat_share
from catch_split_log.activity import seven_days_fight
from catch_split_log.activity import seven_days_lv
from catch_split_log.activity import luxury_sign_split #豪华签到
from util.logs_out_path_of_parse import LOG_PATH

def start_parse(split_date):
    """
        获取并拆分一天的日志
    """
    err=open(LOG_PATH+"%s/%s"%("Error",split_date),'a+')
    nor=open(LOG_PATH+"%s/%s"%("Normal",split_date),'a+')
    sys.stdout=nor
    startime=datetime.datetime.now()
    print 'activity解析开始',startime
    start_list = [friendly_shop, give_me_give_you, max_will, wei_chat_share, seven_days_fight, seven_days_lv, luxury_sign_split]

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
    print 'activity解析结束',endtime
    print 'activity共花费时间',(endtime-startime).seconds,'秒' ,'\n\n'

if __name__ == '__main__':
    if sys.argv[1]:
        start_parse(sys.argv[1])
    else:
        split_date = datetime.date.today() - datetime.timedelta(days=1)
        start_parse(split_date)

