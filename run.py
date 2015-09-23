# -*- coding:utf-8 -*-

__author__ = 'Administrator'
import sys
import os
import datetime
import stat
import parse_all_action_split
import parse_user_detail
import parse_gm_recharge_manage
import parse_active_model
import parse_action_stage
import parse_action_list
import parse_data_search
import parse_union
import parse_activity
import parse_action_rank_list
import parse_all_uid_action_one_file
import parse_number_balance
import parse_statistics_total
import parse_loss_analyse
import parse_user_first_day_keep_play
from util.logs_out_path_of_parse import LOG_PATH



def start(arg):
    parse_all_action_split.start_parse(arg)
    parse_user_detail.start_parse(arg)
    parse_gm_recharge_manage.start_parse(arg)
    parse_active_model.start_parse(arg)
    parse_action_stage.start_parse(arg)
    parse_action_list.start_parse(arg)
    parse_data_search.start_parse(arg)
    parse_union.start_parse(arg)
    parse_activity.start_parse(arg)
    parse_action_rank_list.start_parse(arg)
    parse_all_uid_action_one_file.start_parse(arg)
    parse_number_balance.start_parse(arg)
    parse_loss_analyse.start_parse(arg)
    parse_statistics_total.start(arg)
    parse_user_first_day_keep_play.start_parse(arg)



if __name__ == "__main__":
    os.chmod("/home/ubuntu/data/HaiMaLogParse/", stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
        os.mkdir(LOG_PATH+'Error')
        os.mkdir(LOG_PATH+'Normal')
    startime= datetime.datetime.now()
    print '解析开始',startime,'\n\n\n'
    if len(sys.argv) > 1:
        open(LOG_PATH+'Error/'+sys.argv[1],'w')
        open(LOG_PATH+'Normal/'+sys.argv[1],'w')
        split_date_str = sys.argv[1]
        split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
        start(split_date)
    else:
        arg = datetime.date.today() - datetime.timedelta(days=1)
        open(LOG_PATH+'Error/%s' % arg,'w')
        open(LOG_PATH+'Normal/%s' % arg,'w')
        start(arg)

    endtime=datetime.datetime.now()
    print '解析结束',endtime
    print '共花费时间',(endtime-startime).seconds /60,'分钟','\n\n\n'