# -*- coding:utf-8 -*-

"""
    固定每天抓取拆分日志到当前服务器
    要伴随服务器开启而开启
    GM消费查询
    思路：
        1.筛选行数限制（4G内存大约80000条）
        2.打开多个文件，多次dump到文件
        3.多次load，再一次覆盖dump到原文件，关闭文件
        注：结果 和 表头 同时返回
    输出形式为：
    ALL_NEED_UID_LST:  [uid1,uid2,uid3,uid4,uid4]
    uid1：文件——[[{含有当前UID关键字日志1}...{含有当前UID关键字日志n}],[表头]]
    uid2：文件——[[{含有当前UID关键字日志1}...{含有当前UID关键字日志n}],[表头]]
    uid3：文件——[[{含有当前UID关键字日志1}...{含有当前UID关键字日志n}],[表头]]
"""
import cPickle
import datetime
import sys
import os
import stat
# import urllib2
import time
from util import game_define
from config import game_config
from action.parse_action import log_parse
from util.logs_out_path_of_parse import get_parse_path


LOCAL_LOG_START_DATE = '2015-05-21'
 # TODO：修改每次读取多少行
READ_LINES = 80000

#TODO:             添加需要打出的关键字表
CUR_NEED_LST = [
    'cost_gold',        # 金币消费
    'cost_stone',       # 钻石消费
    'cost_item_list'    # 物品消费列表
]

#TODO：          修改 输出目录 和 UID列表名字
OUT_PUT_FOLDER_NAME = 'gm_cost_search'
NEED_UID_LST_NAME = 'GM_COST_SEARCH_LST'


ALL_NEED_UID_LST = list()   # 需要关键字的UID列表
OPEN_FILES_DICT = dict()    # 文件状态字典 用于文件打开关闭指针偏移操作
def start(split_date):
    """
        获取并拆分一天的日志
    """
    LOCAL_LOG_PATH_NAME_LST, OUT_PUT_PATH_LST = get_parse_path(split_date)

    for index in LOCAL_LOG_PATH_NAME_LST:
        try:
            print split_date, " ", index, "\n"
            # 本地打开
            read_file = LOCAL_LOG_PATH_NAME_LST[index].format(cur_date=split_date)
            #创建目录
            out_put_file_path = OUT_PUT_PATH_LST[index].format(cur_date=split_date, use_path=OUT_PUT_FOLDER_NAME)
            if not os.path.exists(out_put_file_path):
                os.makedirs(out_put_file_path)
            os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
            os.chdir(out_put_file_path)

            start_time = time.time()
            log_lines = open(read_file, 'r')
            end_time = time.time() - start_time
            print "open flie time is:", end_time
            last_line_num = read_flie_last_line(read_file)
            print 'file last line is: ', last_line_num

            if log_lines:
                log_dict_lst = []
                uid_lst = []
                global ALL_NEED_UID_LST
                global OPEN_FILES_DICT
                ALL_NEED_UID_LST = []
                OPEN_FILES_DICT = {}
                start_time = time.time()
                line_err_num = 0
                line_all_num = 0
                for _log_line in log_lines:
                    line_all_num += 1
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    #解析错误返回false 跳过本行
                    if not log_dict:
                        line_err_num += 1
                        continue

                    for key, val in log_dict.items():
                        if key in CUR_NEED_LST:
                            #如果有需要的关键字 就加入总表
                            log_dict_lst.append(log_dict)
                            uid_lst.append(log_dict['uid'])
                            break

                    # TOD:1.限制读取条数
                    if len(log_dict_lst) >= READ_LINES:
                        # print "READ_LINES...... "
                        dump_loop_file(log_dict_lst, uid_lst)  # 到达限制数量dump一次
                        log_dict_lst = []
                        uid_lst = []
                    elif len(log_dict_lst) > 0 and last_line_num == line_all_num:
                        print "last dump_loop_file......   last_line is: ", line_all_num
                        dump_loop_file(log_dict_lst, uid_lst)  # 最后一次dump
                        log_dict_lst = []
                        uid_lst = []
                del log_dict_lst    # del 是自动回收机制 即删除对象是删除引用，只有引用次数为0时才会回收
                print 'err line num is: ', line_err_num
                end_time = time.time() - start_time
                print "filter cur_need_lst all_logs time is:", end_time

                start_time = time.time()
                # TOD:3.循环load 再一次性dump  再关闭每个输出文件
                loop_load_and_once_dump()
                end_time = time.time() - start_time
                print "UID filter and file out time is :", end_time, "\n\n"
        except:
            pass


# dump到各自文件
def dump_loop_file(dict_lst, cur_uid_lst):
    """
    1.更新uid总表 关闭文件时用
    2.open文件. 每次打开新的uid文件 多次dump用
    3.分类并计算数据 结果dump到各自文件
    """
    # 1
    global ALL_NEED_UID_LST
    global OPEN_FILES_DICT
    # 求差集 并更新总表
    different_uid_lst = list(set(cur_uid_lst).difference(set(ALL_NEED_UID_LST)))

    #2
    for uid in different_uid_lst:
        if uid not in ALL_NEED_UID_LST:
            OPEN_FILES_DICT[uid] = open(str(uid), 'w+')

    # 记录玩家列表
    ALL_NEED_UID_LST.extend(different_uid_lst)
    #3
    cur_all_action_dict = dict()
    #将多条数据分为：uid为key，[{}{}{}]为值
    for each_dict in dict_lst:
        cur_all_action_dict.setdefault(each_dict['uid'], []).append(each_dict)

    # dump到每个打开w+模式文件下
    for key_uid, values in cur_all_action_dict.items():
        result_lst = []
        result_lst.extend(log_filter(values, key_uid))
        cPickle.dump(result_lst, OPEN_FILES_DICT[key_uid])


def loop_load_and_once_dump():
    global ALL_NEED_UID_LST
    global OPEN_FILES_DICT

    start_time = time.time()
    for key, flie_path in OPEN_FILES_DICT.items():
        flie_path.seek(0)
        result_loop_lst_values = []     # 返回结果
        result_loop_lst_head = []       # 返回表头

        # 循环load # 每一次[[],[]]
        while True:
            try:
                _tmp_lst = cPickle.load(flie_path)
                result_loop_lst_values.extend(_tmp_lst[0])
                result_loop_lst_head.extend([_tmp_lst[1]])
            except:
                break
        flie_path.seek(0)

        #dump 找最长的表头
        result_head = []
        _head_len = 0
        for each_head in result_loop_lst_head:
            x = len(each_head)
            if x > _head_len:
                result_head = each_head
                _head_len = x

        #once_dump
        cPickle.dump([result_loop_lst_values, result_head], flie_path)
        # time.sleep(1)
        # 关闭文件
        flie_path.close()

    end_time = time.time() - start_time
    print "cPickle once_dump all uid file time is: ", end_time

    # 输出 存在关键字的UID表
    out_put_file = open(NEED_UID_LST_NAME, 'w')
    print out_put_file
    cPickle.dump(ALL_NEED_UID_LST, out_put_file)
    out_put_file.close()


#过滤日志 输出对应UID 服务器
def log_filter(log_dist, uid):
    temp_lst = []
    head_lst = []
    ##输入UID过滤 不输入uid直接返回UID表
    if uid:
        item_lst_len_record = []#物品长度记录
        uid_bool = False
        for each_item in log_dist:
            user_uid = each_item['uid']
            if user_uid == uid:
                uid_bool = True
                user_log_time = each_item['log_time'].strftime("%Y-%m-%d %H:%M:%S")
                user_action_name = game_define.EVENT_LOG_ACTION_DICT[each_item['action']]
                user_cost_gold = each_item.get('cost_gold', 0)
                user_cost_stone = each_item.get('cost_stone', 0)
                user_cost_item_list = each_item.get('cost_item_list', 0)
                # user_server_id = each_item['server_id']
                # user_platform_id = each_item['platform_id']

                row_lst = [
                    user_log_time,
                    user_uid,
                    # user_server_id,
                    # user_platform_id,
                    user_action_name,
                    user_cost_gold,
                    user_cost_stone
                ]
                # print user_cost_item_list , "is" , row_lst
                if user_cost_item_list and len(user_cost_item_list) > 1:
                    item_lst_len_record.append(len(user_cost_item_list))
                    for i in xrange(len(user_cost_item_list)):
                        #将偶数取出变成字符串
                        if i % 2 == 0:
                            # print i, " ", len(user_cost_item_list)
                            if user_cost_item_list[i] > 0:
                                item_tid = int(user_cost_item_list[i])
                                item_config = game_config.get_item_config(item_tid)
                                if item_config:
                                    _name = item_config['name']
                                    user_cost_item_list[i] = _name
                    ##注意：html只会转码第一层列表字符，所以要拆分深层表插入到第一层列表"""
                    #插入物品列表
                    row_lst.extend(user_cost_item_list)
                temp_lst.append(row_lst)

        head_lst = [
            {'width':50,'name':u'消费时间'},
            {'width':50,'name':u'账号UID'},
            # {'width':50,'name':u'服务器ID'},
            # {'width':50,'name':u'平台ID'},
            {'width':50,'name':u'用户事件'},
            {'width':50,'name':u'消耗金币'},
            {'width':50,'name':u'消耗钻石'}
        ]
        item_head_lst = []
        if uid_bool:
            if item_lst_len_record:
                item_lst_max_len = (max(item_lst_len_record) + 1)
                if item_lst_max_len:
                    inum = 0
                    for i in xrange(1, item_lst_max_len):
                        if i % 2 != 0:
                            inum = inum + 1
                            item_head_lst.append({'width': 50, 'name': u'消费物品%d' % inum})
                        else:
                            item_head_lst.append({'width': 50, 'name': u'数量'})

            head_lst.extend(item_head_lst)

    return temp_lst, head_lst


#返回最后一行数
def read_flie_last_line(file_name):
    with open(file_name, 'r') as fh:
        count = 0

        while True:
            buffer = fh.read(1024 * 8192)
            if not buffer:
                break
            count += buffer.count('\n')
        fh.close()

        return count


if __name__ == "__main__":
    start(sys.argv)
