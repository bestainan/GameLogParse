# -*- coding:utf-8 -*-

"""
    解析所有关卡事件
"""
import os
import sys
import datetime
from catch_split_log.action_stage import catch_monster_stage
from catch_split_log.action_stage import exp_stage
from catch_split_log.action_stage import gold_stage
from catch_split_log.action_stage import gym_stage
from catch_split_log.action_stage import hard_stage
from catch_split_log.action_stage import normal_stage
from catch_split_log.action_stage import treasure_battle_stage
from catch_split_log.action_stage import trial_stage
from catch_split_log.action_stage import world_boss_stage
from util.logs_out_in_path import LOG_PATH
from util.logs_out_path_of_parse import LOG_PATH
def start_parse(split_date):
    """
        获取并拆分一天的日志
    """
    if isinstance(split_date,str):
        split_date = datetime.datetime.strptime(split_date, "%Y-%m-%d").date()
    err = open(LOG_PATH+"%s/%s" % ("Error", split_date), 'a+')
    nor = open(LOG_PATH+"%s/%s" % ("Normal", split_date), 'a+')
    sys.stdout=nor
    startime=datetime.datetime.now()
    print 'action_stage解析开始',startime  ,'\n\n'
    start_list = [catch_monster_stage, exp_stage, gold_stage, gym_stage, hard_stage, normal_stage, treasure_battle_stage, trial_stage, world_boss_stage]

    for func in start_list:
        try:
            sys.stdout=nor
            func.start(split_date)
        except Exception,e :
            sys.stdout=err
            print datetime.datetime.now(),str(func),"  Error:",e,"\n"
    sys.stdout=nor

    endtime=datetime.datetime.now()
    print 'action_stage解析结束',endtime
    print 'action_stage共花费时间',(endtime-startime).seconds ,'秒' ,'\n\n'


if __name__ == '__main__':
    if len(sys.argv) > 1:
        split_date_str = sys.argv[1]
        split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
        start_parse(split_date)
    else:
        split_date = datetime.date.today() - datetime.timedelta(days=1)
        start_parse(split_date)
