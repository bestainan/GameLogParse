# -*- coding: utf-8 -*-
__author__ = 'Administrator'
#联盟奖励 ：联盟成员通过‘购买’联盟奖励，来获取物品
import datetime
import pickle
from action.parse_action import log_parse
import os
import stat
import datetime
from config.game_config import get_item_config_with_id_name, get_union_reward_config
from util.logs_out_path_of_parse import get_parse_path
action_equip_lst = []

def start(split_date):
    # dat_lst = []
    # item_name_lst,laji = get_item_config_with_id_name()
    # union_reward_dict = {}
    #
    # # split_date = datetime.datetime.strptime("2015-06-05", "%Y-%m-%d").date()
    # # if args:
    # #     split_date = args
    # # else:
    # #     split_date = datetime.date.today() - datetime.timedelta(days = 1)
    # for i in get_union_reward_config():
    #     if i['itemId']<>0:
    #         union_reward_dict[i['itemId']] = {'price':0,'reward':0,'buy_rate':0,'times':0,'name':''}
    #     elif i['equipmentId']<> 0:
    #         union_reward_dict[i['equipmentId']] = {'price':0,'reward':0,'buy_rate':0,'times':0,'name':''}
    #     else:
    #         union_reward_dict['gold'] = {'price':0,'reward':0,'buy_rate':0,'times':0,'name':''}
    #         union_reward_dict['stone'] = {'price':0,'reward':0,'buy_rate':0,'times':0,'name':''}
    #         union_reward_dict['free_drop'] = {'price':0,'reward':0,'buy_rate':0,'times':0,'name':''}
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST=get_parse_path(split_date)
    for log_path in OUT_PUT_PATH_LST.values():
        try:
            if os.path.exists(log_path.format(cur_date=split_date,use_path = 'all_action')):
                os.chmod(log_path.format(cur_date=split_date,use_path = 'all_action'), stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
                dat_lst = []
                item_name_lst,laji = get_item_config_with_id_name()
                union_reward_dict = {}

                # split_date = datetime.datetime.strptime("2015-06-05", "%Y-%m-%d").date()
                # if args:
                #     split_date = args
                # else:
                #     split_date = datetime.date.today() - datetime.timedelta(days = 1)
                for i in get_union_reward_config():
                    if i['itemId']<>0:
                        union_reward_dict[i['itemId']] = {'price':0,'reward':0,'buy_rate':0,'times':0,'name':''}
                    elif i['equipmentId']<> 0:
                        union_reward_dict[i['equipmentId']] = {'price':0,'reward':0,'buy_rate':0,'times':0,'name':''}
                    else:
                        union_reward_dict['gold'] = {'price':0,'reward':0,'buy_rate':0,'times':0,'name':''}
                        union_reward_dict['stone'] = {'price':0,'reward':0,'buy_rate':0,'times':0,'name':''}
                        union_reward_dict['free_drop'] = {'price':0,'reward':0,'buy_rate':0,'times':0,'name':''}

                buy_times_count = 0
                # union_buy_reward_filepath = log_path+"%s/all_action/%s"%(split_date,'EVENT_ACTION_UNION_BUY_REWARD')
                union_buy_reward_filepath = log_path.format(cur_date=split_date,use_path='all_action')+'EVENT_ACTION_UNION_BUY_REWARD'
                f = open(union_buy_reward_filepath,'r')
                pick_load = pickle.load(f)
                for i in pick_load:
                    # print i
                    if len(i['add_item_list'])<>0:
                        union_reward_dict[i['add_item_list'][0]]['price']+=i['cost_union_point']
                        union_reward_dict[i['add_item_list'][0]]['reward']+=i['add_item_list'][1]
                        union_reward_dict[i['add_item_list'][0]]['times']+=1
                    elif len(i['add_equip_list'])<> 0:
                        union_reward_dict[i['add_equip_list'][0]]['price']+=i['cost_union_point']
                        union_reward_dict[i['add_equip_list'][0]]['reward']+=i['add_equip_list'][1]
                        union_reward_dict[i['add_equip_list'][0]]['times']+=1
                    else:
                        if i['add_gold']<>0:
                            union_reward_dict['gold']['price']+=i['cost_union_point']
                            union_reward_dict['gold']['reward']+=i['add_gold']
                            union_reward_dict['gold']['times']+=1
                        if i['add_stone']<>0:
                            union_reward_dict['stone']['price']+=i['cost_union_point']
                            union_reward_dict['stone']['reward']+=i['add_stone']
                            union_reward_dict['stone']['times']+=1
                        if i['add_free_draw']<>0:
                            union_reward_dict['free_drop']['price']+=i['cost_union_point']
                            union_reward_dict['free_drop']['reward']+=i['add_free_draw']
                            union_reward_dict['free_drop']['times']+=1
                    buy_times_count+=1
                for i in union_reward_dict.keys():
                    if type(i)==int:
                        union_reward_dict[i]['name']=item_name_lst[i]
                    if 'gold'== i :
                        union_reward_dict[i]['name']=u'金币'
                    if 'stone'==i:
                        union_reward_dict[i]['name']=u'钻石'
                    if 'free_drop'==i:
                        union_reward_dict[i]['name']=u'精灵球'
                    try:
                        #print union_reward_dict[i]['times'],buy_times_count
                        union_reward_dict[i]['buy_rate']=str(round(float(union_reward_dict[i]['times'])/float(buy_times_count)*10000)/100)+'%'
                    except:
                       union_reward_dict[i]['buy_rate'] ='0%'
                #print union_reward_dict
                for i in union_reward_dict.values():
                    dat_lst.append([i['name'],i['times'],i['buy_rate'],i['price'],i['reward']])

                # OUT_PUT_FILE_PATH=log_path+"%s/tables/UNION_BUY_REWARD"%(split_date)
                OUT_PUT_FILE_PATH=log_path.format(cur_date=split_date,use_path='tables')+'UNION_BUY_REWARD'
                f=open(OUT_PUT_FILE_PATH,'w')
                pickle.dump(dat_lst,f)
        except Exception,e:
                print datetime.datetime.now(), str('aaa'), "  Error:", e, "\n"

