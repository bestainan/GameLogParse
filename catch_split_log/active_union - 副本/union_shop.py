# -*- coding:utf-8 -*-

import pickle
from action.parse_action import log_parse
import os
import stat
import datetime
from util.game_define import EVENT_LOG_ACTION_SQL_NAME_DICT
from config.game_config import get_union_shop_items_config
from util.logs_out_path_of_parse import get_parse_path

def start(split_date):
    dat_lst=[]
    #split_date = datetime.datetime.strptime("2015-06-05", "%Y-%m-%d").date()
    # if args:
    #     split_date = args
    # else:
    #     split_date = datetime.date.today() - datetime.timedelta(days = 1)
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST=get_parse_path(split_date)
    for log_path in OUT_PUT_PATH_LST.values():

        if os.path.exists(log_path.format(cur_date=split_date,use_path = 'all_action')):
            os.chmod(log_path.format(cur_date=split_date,use_path = 'all_action'), stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
            #total_day=(search_end_date-search_start_date).days+1
            dat_lst=[]
            union_shop_item=get_union_shop_items_config()
            #print union_shop_item
            union_shop_items_dict={}
            for i in union_shop_item.keys():
                union_shop_items_dict[i]={}
                union_shop_items_dict[i]['names']=union_shop_item[i]
                union_shop_items_dict[i]['cost_union_point']=0
                union_shop_items_dict[i]['buy_bodies_sum']=0
                union_shop_items_dict[i]['buy_times_sum']=0
                union_shop_items_dict[i]['buy_rate']=''
                union_shop_items_dict[i]['cost_rate']=''
                union_shop_items_dict[i]['body_rate']=''

            buy_bodies_sum1=0
            buy_times_sum=0
            cost_point_sum=0
            login_device_sum=0

            #cur_date=search_start_date+datetime.timedelta(days=i)
            # union_count_filepath=log_path+"%s/all_action/%s" %(split_date,'EVENT_ACTION_UNION_SHOP_BUY')
            # print log_path.format(cur_date = split_date,use_path = 'all_action')
            union_count_filepath=log_path.format(cur_date = split_date,use_path = 'all_action')+'EVENT_ACTION_UNION_SHOP_BUY'

            f=open(union_count_filepath,'r')
            pick_load=pickle.load(f)
            buy_bodies_sum={}
            every_buy_bodies_sum_dict={}
            every_buy_times_sum_dict={}
            every_cost_point_sum_dict={}

            for i in union_shop_item.keys():
                every_buy_bodies_sum_dict[i]={}
                every_buy_times_sum_dict[i]=0
                every_cost_point_sum_dict[i]=0
            for i in pick_load:
                buy_bodies_sum[i['uid']]=1
                # i
                every_buy_bodies_sum_dict[i['add_item_list'][0]][i['uid']]=1
                every_buy_times_sum_dict[i['add_item_list'][0]]+=1
                every_cost_point_sum_dict[i['add_item_list'][0]]+=i['cost_union_point']

            for i in union_shop_item.keys():
                buy_bodies_sum1+=len(every_buy_bodies_sum_dict[i])
                union_shop_items_dict[i]['buy_bodies_sum']=len(every_buy_bodies_sum_dict[i])
                #print len(every_buy_bodies_sum_dict[i])
                cost_point_sum+=every_cost_point_sum_dict[i]
                union_shop_items_dict[i]['cost_union_point']=every_cost_point_sum_dict[i]
                buy_times_sum+=every_buy_times_sum_dict[i]
                union_shop_items_dict[i]['buy_times_sum']=every_buy_times_sum_dict[i]
            #print buy_bodies_sum1,cost_point_sum,buy_times_sum
            # login_device_sum_filepath=log_path+"%s/all_action/%s" %(split_date,'EVENT_ACTION_ROLE_LOGIN')
            login_device_sum_filepath = log_path.format(cur_date=split_date,use_path='all_action')+'EVENT_ACTION_ROLE_LOGIN'
            # print login_device_sum_filepath,'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
            f=open(login_device_sum_filepath,'r')
            pick_load=pickle.load(f)
            login_device_sum_dict={}
            for i in pick_load:
                login_device_sum_dict[i['dev_id']]=1
            #print login_device_sum_dict
            login_device_sum=len(login_device_sum_dict)
            #print login_device_sum


            for i in union_shop_item.keys():
                try:
                    union_shop_items_dict[i]['buy_rate']=str(round(float(union_shop_items_dict[i]['buy_bodies_sum'])/float(login_device_sum)*10000)/100)+'%'
                except:
                    union_shop_items_dict[i]['buy_rate']='0%'
                try:
                    union_shop_items_dict[i]['cost_rate']=str(round(float(union_shop_items_dict[i]['cost_union_point'])/float(cost_point_sum)*10000)/100)+'%'
                except:
                    union_shop_items_dict[i]['cost_rate']='0%'
                try:
                    union_shop_items_dict[i]['body_rate']=str(round(float(union_shop_items_dict[i]['buy_bodies_sum'])/float(buy_bodies_sum1)*10000)/100)+'%'
                except:
                    union_shop_items_dict[i]['body_rate']='0%'

            for i in union_shop_items_dict.values():
                dat_lst.append([i['names'],i['cost_union_point'],i['buy_bodies_sum'],i['buy_times_sum'],i['buy_rate'],i['cost_rate'],i['body_rate']])

            if not os.path.exists(log_path.format(cur_date=split_date,use_path='tables')):
                os.mkdir(log_path.format(cur_date=split_date,use_path='tables'))
            # OUT_PUT_FILE_PATH=log_path+"%s/tables/%s"%(split_date,'UNION_SHOP')
            OUT_PUT_FILE_PATH=log_path.format(cur_date=split_date,use_path='tables')+'UNION_SHOP'
            f=open(OUT_PUT_FILE_PATH,'w')

            pickle.dump(dat_lst,f)



# def get_union_shop_items_config():
#     all_items=get_item_config_with_id_name()
#     _item_dict={}
#     _item_config=open( ITEMS_CONFIG_PATH+'union_shop_config','r')
#     for item in _item_config.values():
#         _item_dict[item['item']]=all_items[item['item']]
#     return _item_dict
#
# def get_item_config_with_id_name():
#     _item_config = open( ITEMS_CONFIG_PATH+'/items_config.py','r')
#     _re_item = dict()
#     for item in _item_config:
#         _re_item[item['id']] = item['name']
#     return _re_item

