# -*- coding:utf-8 -*-
import pickle
from action.parse_action import log_parse
import os
import stat
import datetime
from util.game_define import EVENT_LOG_ACTION_SQL_NAME_DICT,EVENT_LOG_ACTION_DICT
from util.logs_out_path_of_parse import get_parse_path
from tempfile import TemporaryFile

"""对用户获得物品进行统计，如GM发放或用户自己‘花费’获得
"""

get_item_save_dict={
    'add_gold':u'金币',
    'add_stone':u'钻石',
    'add_free_draw':u'精灵球',
    'add_gym_point':u'道馆币',
    'add_consumption_point':u'消费积分',
    'add_arena_emblem':u'纹章',
    'add_world_boss_point':u'战魂',
    'add_universal_fragment':u'万能碎片',
    'add_union_point':u'联盟币',
    'add_item_list':u'其它'

}

"""对可消费的物品获得纪录进行统计
    统计项包括“钻石、金币、精灵球、道馆币、消费积分、纹章、战魂、万能碎片、联盟币、其它”，共10项
    输出结果为“日期、角色名、使用时间、物品名称、数量”
"""


#
# OUT_PUT_PATH = "/zgame/FeiLiuLogParse/data/"
# LOG_SERVER_PATH = "/zgame/FeiLiuLogs/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"
# #LOG_SERVER_PATH = "/zgame/HaiMaLogs/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"
# CATCH_SQL_PAS = "Zgamecn6"
# LOCAL_LOG_START_DATE = '2015-05-21'
# action_equip_lst = []

#from util.game_define import CATCH_LOGS_DAT
from config.game_config import get_item_config_with_id_name
#def start(args):
def start(split_date):
    """
        获取并拆分一天的日志
    """
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST=get_parse_path(split_date)
    for log_path in LOCAL_LOG_PATH_NAME_LST.keys():
        try:
            item_name_config_dict,laji=get_item_config_with_id_name()
            url_path = LOCAL_LOG_PATH_NAME_LST[log_path].format(cur_date=split_date)
            url = open(url_path,'r')
            output_path=OUT_PUT_PATH_LST[log_path].format(cur_date=split_date,use_path='user_get_log')
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            for i in os.listdir(output_path):
                os.remove(output_path+i)
            if url:
                log_lines = url.readlines()
                datetime.datetime.now()
                print 'readlines done',len(log_lines)
                for _log_line in log_lines:
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    result=_user_get_log(log_dict)
                    # print len(result)
                    if result:
                        temp=''
                        item_str=''
                        sum_str=''
                        for result_key in result:
                            if result_key in get_item_save_dict.keys():
                                if result_key=='add_item_list':
                                    z=0
                                    while z < len(result['add_item_list']):
                                        if result['add_item_list'][z+1] != 0 :
                                            item_str+=item_name_config_dict[int(result['add_item_list'][z])] +','
                                            sum_str+=str(result['add_item_list'][z+1])+','
                                            z+=2
                                else:
                                    if int(result[result_key]) !=0 :
                                        item_str += get_item_save_dict[result_key] +','
                                        sum_str+=str(result[result_key])+','
                        sum_str=sum_str.rstrip(',')
                        item_str=item_str.rstrip(',')
                        if item_str != '':
                            temp+=str([str(result['log_time']),result['uid'],item_str,sum_str,EVENT_LOG_ACTION_DICT[result['action']]])+'\n'
                            output_file_path=open(output_path+str(result['uid']),'a+')
                            output_file_path.write(temp)
                            output_file_path.flush()
                            #pickle.dump(temp,output_file_path)
                            output_file_path.close()
        except Exception,e:
            print datetime.datetime.now(), str('all_action_split'), "  Error:", e, "\n"


        print 'work done',datetime.datetime.now(),log_path

def _user_get_log(log_dict):
    # try:
    #     for j in log_dict.keys()[7:]:
    #         if j in get_item_save_dict.keys():
    #             return log_dict
    # except:
    #     return
    try :
        if len(set(log_dict.keys()) & set(get_item_save_dict.keys())) >0:
            return log_dict
        else:
            return
    except:
        return


