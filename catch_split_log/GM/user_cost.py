# -*- coding:utf-8 -*-
import pickle
import datetime
import sys
import os
import stat
from action.parse_action import log_parse
from util.game_define import  EVENT_LOG_ACTION_DICT
from config.game_config import get_item_config_with_id_name
from util.logs_out_path_of_parse import get_parse_path
item_name_dict,laji=get_item_config_with_id_name()
cost_item_save_dict={
    'cost_gold':'金币',
    'cost_stone':'钻石',
    'cost_free_draw':'精灵球',
    'cost_gym_point':'道馆币',
    'cost_consumption_point':'消费积分',
    'cost_arena_emblem':'纹章',
    'cost_world_boss_point':'战魂',
    'cost_universal_fragment':'万能碎片',
    'cost_union_point':'联盟币',


}

"""对可消费的物品消费纪录进行统计
    统计项包括“钻石、金币、精灵球、道馆币、消费积分、纹章、战魂、万能碎片”，共8项
    输出结果为“日期、角色名、使用时间、物品名称、数量”
"""



# OUT_PUT_PATH = "/zgame/FeiLiuLogParse/data/"
# LOG_SERVER_PATH = "/zgame/FeiLiuLogs/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"
# #LOG_SERVER_PATH = "/zgame/HaiMaLogs/PIKA_pc_event_%s/PIKA_pc_event_%s_00000"
# CATCH_SQL_PAS = "Zgamecn6"
# LOCAL_LOG_START_DATE = '2015-05-21'
# EQUIP_ACTION_LST = ['add_equip_list', 'remove_equip_list']
# action_equip_lst = []


#def start(args):
def start(split_date):
    """
        获取并拆分一天的日志
    """
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST=get_parse_path(split_date)
    for log_path in LOCAL_LOG_PATH_NAME_LST.keys():
         try:
            print(split_date)
            url_path = LOCAL_LOG_PATH_NAME_LST[log_path].format(cur_date=split_date)
            url = open(url_path,'r')
            output_path=OUT_PUT_PATH_LST[log_path].format(cur_date=split_date,use_path='user_cost_log')
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            for i in os.listdir(output_path):
                os.remove(output_path+i)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            if url:
                log_lines = url.readlines()
                datetime.datetime.now()
                for _log_line in log_lines:
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    result=_user_cost_log(log_dict)
                    # print len(result)
                    if result:
                        temp=''
                        item_str=''
                        sum_str=''
                        for result_key in result:
                            if result_key in cost_item_save_dict.keys():
                                if int(result[result_key]) !=0 :
                                    item_str += cost_item_save_dict[result_key] +','
                                    sum_str+=str(result[result_key])+','
                        sum_str=sum_str.rstrip(',')
                        item_str=item_str.rstrip(',')
                        if item_str != '':
                            temp+=str([str(result['log_time']),result['uid'],item_str,sum_str,EVENT_LOG_ACTION_DICT[result['action']]])+'\n'
                            output_file_path=open(output_path+str(result['uid']),'a+')
                            output_file_path.write(temp)
                            output_file_path.flush()
                            output_file_path.close()
         except Exception,e:
            print datetime.datetime.now(), str('all_action_split'), "  Error:", e, "\n"
        #     log_lines = url.readlines()
        #     for _log_line in log_lines:
        #         _log_line = _log_line.strip()
        #         log_dict = log_parse(_log_line)
        #         result=_user_cost_log(split_date,log_dict)
        #         if result:
        #             if result['uid'] in user_cost_dict.keys():
        #                 user_cost_dict[result['uid']].append(result)
        #             else:
        #                 user_cost_dict[result['uid']]=[]
        #                 user_cost_dict[result['uid']].append(result)
        # print 'i work done.'
        # print len(user_cost_dict)
        # OUT_PUT_FILE=OUT_PUT_PATH_LST[log_path]+'%s/%s'%(split_date,'user_cost_log/')
        # #print OUT_PUT_FILE
        # if not os.path.exists(OUT_PUT_FILE):
        #     os.makedirs(OUT_PUT_FILE)
        # for i in user_cost_dict.items():
        #     temp=[]
        #     for j in i[1]:
        #         #print j ,'j'
        #         for x in j.keys()[7:]:
        #             #print x
        #             if x in cost_item_save_dict.keys() and j[x]!=0:
        #                 temp.append([str(j['log_time']),j['uid'],EVENT_LOG_ACTION_DICT[j['action']],cost_item_save_dict[x],j[x]])
        #     pickle.dump(temp,open(OUT_PUT_FILE+str(i[0]),'w'))

        # for i in user_cost_dict.items():
        #     print i
        #     a=input()




        # for i in user_cost_dict.items():
        #     pickle.dump(i[1],open(OUT_PUT_FILE+str(i[0]),'w'))
        #pickle.dump(user_cost_dict,f)


def _user_cost_log(log_dict):
        try:
            for j in log_dict.keys():
                if j in cost_item_save_dict.keys():
                    return log_dict
                    break
        except:
            return

