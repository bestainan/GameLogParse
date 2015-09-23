# -*- coding:utf-8 -*-


import datetime
import pickle
from action.parse_action import log_parse
import os
import stat
import datetime
from util.logs_out_path_of_parse import get_parse_path

def start(split_date):
    dat_lst=[]
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST=get_parse_path(split_date)
    for log_path in OUT_PUT_PATH_LST.values():
        if os.path.exists(log_path.format(cur_date=split_date,use_path = 'all_action')):
            os.chmod(log_path.format(cur_date=split_date,use_path = 'all_action'), stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
            #total_day=(search_end_date-search_start_date).days+1
            # if args:
            #     split_date = args
            # else:
            #     split_date = datetime.date.today() - datetime.timedelta(days = 1)
            #split_date = datetime.date.today() - datetime.timedelta(days=1)

            normal_sign_count=0
            senior_sign_count=0
            luxury_sign_count=0
            normal_sign_count_cost_gold=0
            senior_sign_count_cost_stone=0
            luxury_sign_count_cost_stone=0
            as_sign_union_cost=0
            count1=0
            count2=0
            count3=0
            count4=0

            # union_count_filepath=log_path+"%s/all_action/%s" %(split_date,'EVENT_ACTION_UNION_SIGN')

            # print split_date
            union_count_filepath=log_path.format(cur_date=split_date,use_path='all_action')+'EVENT_ACTION_UNION_SIGN'
            # print union_count_filepath,'uniounion_count_filepathn_'
            f=open(union_count_filepath,'r')
            temp=pickle.load(f)
            for i in temp:
                if i['union_sign_type']==1:
                    normal_sign_count+=1
                    normal_sign_count_cost_gold+=i['cost_gold']
                if i['union_sign_type']==2:
                    senior_sign_count+=1
                    senior_sign_count_cost_stone+=i['cost_stone']
                if i['union_sign_type']==3:
                    luxury_sign_count+=1
                    luxury_sign_count_cost_stone+=i['cost_stone']
                as_sign_union_cost+=i['add_union_point']
            f.close()
            union_reward_count_filepath=log_path.format(cur_date=split_date,use_path='all_action')+'EVENT_ACTION_UNION_SIGN_REWARD'
            # print union_reward_count_filepath,'fdsaffffffffffffffffffffffffffffffff'
            f=open(union_reward_count_filepath,'r')
            temp=pickle.load(f)
            for i in temp:
                # print i
                # a=input()
                as_sign_union_cost+=i['add_union_point']
                if len(i['add_item_list'])<>0:
                    count1+=i['add_item_list'][1]
                count2+=i['add_gold']
                count3+=i['add_union_point']
                count4+=i['add_stone']
            f.close()
            dat_lst.append([str(split_date),normal_sign_count,senior_sign_count,luxury_sign_count,normal_sign_count_cost_gold,senior_sign_count_cost_stone,luxury_sign_count_cost_stone,as_sign_union_cost,count1,count2,count3,count4])
            if not os.path.exists(log_path.format(cur_date=split_date,use_path='tables')):
                os.mkdir(log_path.format(cur_date=split_date,use_path='tables'))
            OUT_PUT_FILE_PATH=log_path.format(cur_date=split_date,use_path='tables')+'UNION_SIGN'
            f=open(OUT_PUT_FILE_PATH,'w')
            pickle.dump(dat_lst,f)


