# -*- coding:utf-8 -*-

import pickle
import os
import stat
import datetime
from util.logs_out_path_of_parse import get_parse_path


#联盟信息  ，计算每天的联盟信息

def start(split_date):
    """
        获取并拆分一天的日志
    """
    # split_date = datetime.datetime.strptime("2015-06-05", "%Y-%m-%d").date()
    # if args:
    #     split_date = args
    # else:
    #     split_date = datetime.date.today() - datetime.timedelta(days = 1)

    union_count=0
    union_cost_stone_count=0
    union_apply_count=0
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST=get_parse_path(split_date)
    for log_path in OUT_PUT_PATH_LST.values():
        try:
            if os.path.exists(log_path.format(cur_date=split_date,use_path = 'all_action')):
                dat_lst=[]
                os.chmod(log_path.format(cur_date=split_date,use_path = 'all_action'), stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
                union_cost_stone_count=0
                union_apply_count=0
                union_accept_count=0


                # union_count_filepath=log_path+"%s/all_action/%s" %(split_date,'EVENT_ACTION_UNION_CREATE')
                union_count_filepath=log_path.format(cur_date=split_date,use_path='all_action')+'EVENT_ACTION_UNION_CREATE'
                f=open(union_count_filepath,'r')
                temp=pickle.load(f)
                union_count=len(temp)
                for i in temp:
                    union_cost_stone_count+=i['cost_stone']
                f.close()
                # union_apply_count_filepath=log_path+"%s/all_action/%s" %(split_date,'EVENT_ACTION_UNION_APPLY_JOIN')
                union_apply_count_filepath=log_path.format(cur_date=split_date,use_path='all_action')+'EVENT_ACTION_UNION_APPLY_JOIN'
                f=open(union_apply_count_filepath,'r')
                temp=pickle.load(f)
                union_apply_count=len(temp)
                f.close()
                # union_accept_count_filepath=log_path+"%s/all_action/%s" %(split_date,'EVENT_ACTION_UNION_ACCEPT_ADD_MEMBER')
                union_accept_count_filepath=log_path.format(cur_date=split_date,use_path='all_action')+'EVENT_ACTION_UNION_ACCEPT_ADD_MEMBER'
                f=open(union_accept_count_filepath,'r')
                temp=pickle.load(f)
                union_accept_count=len(temp)
                f.close()

                # player_login_filepath=log_path+"%s/tables/%s" %(split_date,'USER_DETAIL')
                player_login_filepath=log_path.format(cur_date=split_date,use_path='tables')+'USER_DETAIL'
                f=open(player_login_filepath,'r')
                temp=pickle.load(f)
                union_open_count=0
                for i in temp.values():
                    if i['level']>= 25:
                        union_open_count+=1
                try:
                    success_rate=str(round(float(union_accept_count)/float(union_apply_count)*10000)/100)+'%'
                except:
                    success_rate='0%'
                try:
                    union_open_rate=str(round(float(union_accept_count+union_count)/float(union_open_count)*10000)/100)+'%'
                except:
                    union_open_rate='0%'
                # 时间，创建联萌人数，创建联萌消耗钻石，申请联萌人数，申请联萌成功人数，申请联萌成功率，联萌功能开启人数，进入联萌人数占比
                dat_lst.append([str(split_date),union_count,union_cost_stone_count,union_apply_count,union_accept_count,success_rate,union_open_count,union_open_rate])


                # if not os._exists(CATCH_LOGS_DAT+"/data/%s/union/"%(split_date)):
                if not os.path.exists(log_path.format(cur_date=split_date,use_path='tables')):
                    os.mkdir(log_path.format(cur_date=split_date,use_path='tables'))
                # OUT_PUT_FILE_PATH=log_path+"%s/tables/UNION_COUNT"%(split_date)
                OUT_PUT_FILE_PATH=log_path.format(cur_date=split_date,use_path='tables')+'UNION_COUNT'
                f=open(OUT_PUT_FILE_PATH,'w')
                pickle.dump(dat_lst,f)
        except Exception,e:
            print datetime.datetime.now(), str('all_action_split'), "  Error:", e, "\n"


