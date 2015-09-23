# -*- coding:utf-8 -*-
import pickle
from action.parse_action import log_parse
import os
import stat
import datetime
from util.game_define import EVENT_LOG_ACTION_SQL_NAME_DICT
from config.game_config import get_union_shop_items_config
from config.game_config import get_union_big_stage_name_config,get_union_little_stage_name_config
from util.logs_out_path_of_parse import get_parse_path

#联盟关卡
def start(split_date):

    #split_date=datetime.datetime.strptime("2015-06-05", "%Y-%m-%d").date()
    # if args:
    #     split_date = args
    # else:
    #     split_date = datetime.date.today() - datetime.timedelta(days = 1)
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST=get_parse_path(split_date)
    for log_path in OUT_PUT_PATH_LST.values():
        if os.path.exists(log_path.format(cur_date=split_date,use_path = 'all_action')):
            dat_lst=[]
            os.chmod(log_path.format(cur_date=split_date,use_path = 'all_action'), stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
            big_stage_name_lst=get_union_big_stage_name_config()
            union_stage_compare_dict=dict() #提取大关与小关对应关系，生成文件形式{大关：{小关id1:name,id2:name,id3:name,……}}
            union_stage_reverse_compare_dict=dict()
            union_big_stage_name_dict=dict()#获取大关的名字
            union_stage_name_dict=dict()
            #union_big_stage_every_sum_dict=dict() #获取每个大关的副本开启次数
            union_first_dict={}
            union_next_dict={}
            stage_name_dict=get_union_little_stage_name_config()
            #print stage_name_dict
            #获取大关与小关的对照表
            for i in big_stage_name_lst:
                union_stage_compare_dict[i['id']]={}
                union_big_stage_name_dict[i['id']]=i['name']
                for j in i :
                    if 'mission' in j :
                        #print i[j]
                        union_stage_compare_dict[i['id']][i[j]]=stage_name_dict[str(i[j])]
            #print union_stage_compare_dict
    
            for i in union_stage_compare_dict.values():
                union_stage_name_dict.update(i)
    
            #print union_stage_name_dict
    
            #小关与大关的反向对照表
            for i in  union_stage_compare_dict.keys():
                for j in union_stage_compare_dict[i].keys():
                    union_stage_reverse_compare_dict[j]=i
    
    
            #将表格分成了两份，union_firest_dict为副本统计
            for i in union_big_stage_name_dict.keys():
                union_first_dict[i]={}
                union_first_dict[i]['name']=union_big_stage_name_dict[i]
                union_first_dict[i]['open_sum']=0
                union_first_dict[i]['cross_sum']=0
                union_first_dict[i]['open_rate']=''
                union_first_dict[i]['corss_rate']=''
    
            #union_next_dict 定义
            for i in union_stage_reverse_compare_dict.keys():
                union_next_dict[i]={}
                union_next_dict[i]['name']=union_stage_name_dict[i]
                #print union_next_dict[i]['name']
                union_next_dict[i]['join_times']=0
                union_next_dict[i]['body_times']=0
                union_next_dict[i]['cross_times']=0
    
            open_sum=0
    
    
            #副本总的开启次数
            union_big_stage_open_sum=0
            #每个副本的开启人数(只有会长才可以去选择打哪个副本，并且每天只能打一个，所以只要保持UNION_UID唯一即可，下同
            union_every_big_stage_open_sum_dict=dict()
            for temp in union_big_stage_name_dict.keys():
                union_every_big_stage_open_sum_dict[temp]={}
    
            #副本通关次数
            union_every_big_stage_cross_sum_dict={}
            for temp in union_big_stage_name_dict.keys():
                union_every_big_stage_cross_sum_dict[temp]={}
            #关卡的参与次数
            union_stage_join_sum=0
            # for temp in union_stage_name_dict:
            # 	union_stage_join_sum_dict[temp.keys()]={}
            #关卡参与人数
            union_stage_body_join_sum_dict=dict()
            for temp in union_stage_name_dict.keys():
                union_stage_body_join_sum_dict[temp]={}
            #关卡通关次数
            union_stage_cross_sum_dict=dict()
            for temp in union_stage_name_dict.keys():
                union_stage_cross_sum_dict[temp]=0
    
            #小关参与次数
            union_stage_join_sum_dict={}
            for i in union_stage_reverse_compare_dict.keys():
                union_stage_join_sum_dict[i]=0

            #大关通关率
            # union_big_stage_open_sum={}
            # for i in union_big_stage_name_dict.keys():
            #     union_big_stage_name_dict[i]=0
            #计算部分
            union_count_filepath=log_path.format(cur_date=split_date,use_path='all_action')+'EVENT_ACTION_UNION_ATTACK_STAGE'
            f=open(union_count_filepath,'r')
            pick_load=pickle.load(f)
            for pick_open_temp in pick_load:
                #大关计算部分
                #print pick_open_temp['stage_index']
                if pick_open_temp['stage_index'] in union_stage_reverse_compare_dict.keys():
                    union_every_big_stage_open_sum_dict[union_stage_reverse_compare_dict[pick_open_temp['stage_index']]][pick_open_temp['uid']]=1
                if pick_open_temp['union_all_hp']==0:
                    union_every_big_stage_cross_sum_dict[union_stage_reverse_compare_dict[pick_open_temp['stage_index']]][pick_open_temp['uid']]=0
    
                #小关计算部分
                union_stage_join_sum_dict[pick_open_temp['stage_index']]+=1
                union_stage_body_join_sum_dict[pick_open_temp['stage_index']][pick_open_temp['uid']]=0
                if pick_open_temp['union_stage_hp']==0:
                    union_stage_cross_sum_dict[pick_open_temp['stage_index']]+=1
            #print union_stage_body_join_sum_dict
            #print union_every_big_stage_cross_sum_dict,union_stage_cross_sum_dict,union_big_stage_open_sum
            for sum in union_every_big_stage_open_sum_dict.values():
                open_sum+=len(sum)
    
            open_sum+=union_big_stage_open_sum
            for i in union_big_stage_name_dict.keys():
                union_first_dict[i]['open_sum']=len(union_every_big_stage_open_sum_dict[i])
                union_first_dict[i]['cross_sum']=len(union_every_big_stage_cross_sum_dict[i])
            for i in union_stage_name_dict.keys():
                union_next_dict[i]['join_times']=union_stage_join_sum_dict[i]
                union_next_dict[i]['body_times']=len(union_stage_body_join_sum_dict[i])
                #print union_next_dict[i]['body_times']
                union_next_dict[i]['cross_times']=union_stage_cross_sum_dict[i]
    
            for i in union_big_stage_name_dict.keys():
                try:
                    #print union_first_dict[i]['open_sum'],open_sum
                    union_first_dict[i]['open_rate']=str(round(float(union_first_dict[i]['open_sum'])/float(open_sum)*10000)/100)+'%'
                except:
                     union_first_dict[i]['open_rate']='0%'
                try:
                    union_first_dict[i]['cross_rate']=str(round(float(union_first_dict[i]['cross_sum'])/float(union_first_dict[i]['open_sum'])*10000)/100)+'%'
                except:
                    union_first_dict[i]['cross_rate']='0%'
            # for i in union_stage_name_dict:
            # 	dat_lst.append([union_first_dict[i.keys()]['name'],union_first_dict[i.keys()]['open_sum'],union_first_dict[i.keys()]['open_rate'],union_first_dict[i.keys()]['cross_sum']])
            for i in union_stage_reverse_compare_dict.items():
                dat_lst.append([
                    union_first_dict[i[1]]['name'],union_first_dict[i[1]]['open_sum'],union_first_dict[i[1]]['open_rate'],union_first_dict[i[1]]['cross_sum'],union_first_dict[i[1]]['cross_rate'],
                    union_next_dict[i[0]]['name'],union_next_dict[i[0]]['join_times'],union_next_dict[i[0]]['body_times'],union_next_dict[i[0]]['cross_times'],
                ])
                #print union_next_dict[i[0]]['name']
    
            #print dat_lst
            if not os.path.exists(log_path.format(cur_date=split_date,use_path='tables')):
                os.mkdir(log_path.format(cur_date=split_date,use_path='tables'))
            OUT_PUT_FILE_PATH=log_path.format(cur_date=split_date,use_path='tables')+'UNION_STAGE'
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

