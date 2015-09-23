# -*- coding:utf-8 -*-

"""
    固定每天抓取拆分日志到当前服务器
    要伴随服务器开启而开启
    特殊分离行为
"""
import cPickle
import datetime
import sys
import os
import stat
import time
from util import game_define
from action.parse_action import log_parse
from util.logs_out_path_of_parse import get_parse_path
from action.parse_action import all_action_dict
from util.logs_out_path_of_parse import LOG_PATH

LOCAL_LOG_START_DATE = '2015-05-21'

OUT_PUT_FOLDER_NAME = "all_action"
RESULT_LOOP_LST = []     # 多次load加入此表
 # TODO：修改每次读取多少行
READ_LINES = 800000


def start_parse(split_date):
    """
        获取并拆分一天的日志
        总体思路：1.共读一次，分析每行，是哪种action，就dump到哪个文件下（187个文件）
                  2.多次dump，但收集READ_LINES行后才会dump （缓冲池）尽量减少dump次数的前提下选取最小时间消耗
                  3.读完所有行后，循环多次去读dump的文件（多次load），再一次dump到原文件中（指针到0）
            注：  经测试得出结论：dump次数越多文件越大,所以避免dump次数太多
    """
    err = open(LOG_PATH+"%s/%s" % ("Error", split_date), 'a+')
    nor = open(LOG_PATH+"%s/%s" % ("Normal", split_date), 'a+')
    # print err,nor
    sys.stdout = nor
    startime = datetime.datetime.now()
    print 'all_action_split解析开始', startime, '\n\n'
    LOCAL_LOG_PATH_NAME_LST , OUT_PUT_PATH_LST = get_parse_path(split_date)

    for index in LOCAL_LOG_PATH_NAME_LST:
        sys.stdout = nor
        print split_date, " ", index, "\n"
        # 本地打开
        read_file = LOCAL_LOG_PATH_NAME_LST[index].format(cur_date=split_date)
        start_time = time.time()
        try:
            log_lines = open(read_file, 'r')
            end_time = time.time() - start_time
            print "open flie time is:", end_time
            last_line_num = read_flie_last_line(read_file)
            print last_line_num

            #创建目录
            out_put_file_path = OUT_PUT_PATH_LST[index].format(cur_date=split_date, use_path=OUT_PUT_FOLDER_NAME)
            if not os.path.exists(out_put_file_path):
                os.makedirs(out_put_file_path)
            os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
            # TOD：0.打开创建并打开所有文件w+模式 # 切换路径到all_action  输出不是此文件夹的文件别忘了切换
            os.chdir(out_put_file_path)
            _open_files_dict_ = dict()
            for key in all_action_dict.keys():
                _open_files_dict_[key] = open(game_define.EVENT_LOG_ACTION_SQL_NAME_DICT[key], 'w+')

            if log_lines:
                log_dict_lst = []
                log_lines.seek(0)
                line_all_num = 0
                start_time = time.time()
                for _log_line in log_lines:
                    line_all_num += 1
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    #容错处理
                    if not log_dict:
                        sys.stdout = err
                        #TODO 开启注释 查数据错误
                        print _log_line, "______", index
                        continue
                    else:
                        sys.stdout = nor

                    log_dict_lst.append(log_dict)
                    # TOD:1.建立缓存限制，限制读取条数
                    if len(log_dict_lst) >= READ_LINES:
                        dump_loop_file(log_dict_lst, _open_files_dict_)  # 到达限制数量dump一次
                        log_dict_lst = []
                    elif len(log_dict_lst) > 0 and last_line_num == line_all_num:
                        print "this is last dump_loop_file"
                        dump_loop_file(log_dict_lst, _open_files_dict_)  # 最后一次dump
                        log_dict_lst = []
                del log_dict_lst    # del 是自动回收机制 即删除对象是删除引用，只有引用次数为0时才会回收
                #到此时 一个日志读完 并多次dump完
                end_time = time.time() - start_time
                print "ation compute and dump_loop  time is:", end_time

                # TOD:3.循环load 再一次性dump  再关闭每个输出文件
                _action_id_lst = []
                start_time = time.time()
                for key, values in _open_files_dict_.items():
                    values.seek(0)
                    global RESULT_LOOP_LST
                    RESULT_LOOP_LST = []

                    # 循环load
                    while True:
                        try:
                            RESULT_LOOP_LST.extend(cPickle.load(values))
                        except:
                            break
                    '''至关重要的一步，w+模式是读写模式 覆盖写入的时候要知道指针位置'''
                    values.seek(0)

                    #dump
                    cPickle.dump(RESULT_LOOP_LST, values)
                     # # time.sleep(1)
                    # 关闭文件
                    values.close()
                    _action_id_lst.extend([key, game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(key, 'Err')])

                    #GM后台数据计算输出 会员管理—充值查询
                    if game_define.EVENT_ACTION_RECHARGE_PLAYER == key:  # 如果是外部充值 筛选数据
                        #创建目录
                        out_put_file_path = OUT_PUT_PATH_LST[index].format(cur_date=split_date, use_path='tables')
                        if not os.path.exists(out_put_file_path):
                            os.makedirs(out_put_file_path)
                        os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)
                        log_filter_EVENT_ACTION_RECHARGE_PLAYER(RESULT_LOOP_LST, out_put_file_path)
                    del RESULT_LOOP_LST
            #关闭日志文件
            log_lines.close()
            end_time = time.time() - start_time
            print "cPickle cur_server dump name list is: \n", _action_id_lst, '\n'
            print " and time is: ", end_time, "-------------------------------------server  ", index, "\n\n"

        except Exception, e:
            sys.stdout = err
            print datetime.datetime.now(), str('all_action_split'), "  Error:", e, "\n"
            pass

    sys.stdout = nor
    endtime = datetime.datetime.now()
    print 'all_action_split解析结束', endtime
    print 'all_action_split共花费时间', (endtime-startime).seconds, '秒', '\n\n'


# dump到各自文件
def dump_loop_file(dict_lst, files_dict):
    cur_all_action_dict = dict()
    #将多条数据分为：事件id为key，[{}{}{}]为值
    for each_dict in dict_lst:
        cur_all_action_dict.setdefault(each_dict['action'], []).append(each_dict)

    # dump到每个打开w+模式文件下
    for key, values in cur_all_action_dict.items():
        cPickle.dump(values, files_dict[key])

#返回最后一行日志进行比较  测试1G文件 读取很快
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


def log_filter_EVENT_ACTION_RECHARGE_PLAYER(dict_lst, out_put_path):
    """
    GM充值管理 充值查询
    """
    start_time = time.time()
    temp_dict = {}
    for each_item in dict_lst:
        user_log_time = each_item['log_time'].strftime("%Y-%m-%d %H:%M:%S")
        user_uid = each_item['uid']
        user_add_rmb = each_item['add_rmb']
        user_order_id = each_item['order_id']
        user_old_rmb = int(each_item['old_rmb'])
        user_server_id = int(each_item['server_id'])
        user_platform_id = int(each_item['platform_id'])

        if user_old_rmb == 0:
            user_first_cost = "是"
        else:
            user_first_cost = "否"

        ser_lst, platform_lst = _get_server_list()
        user_ser_str, user_platform_str = "", ""
        for each_ser_dict, each_plat_dict in zip(ser_lst, platform_lst):
            if user_platform_id == int(each_plat_dict['id']):
                user_platform_str = each_plat_dict['name']
            if user_server_id == int(each_ser_dict['id']):
                user_ser_str = each_ser_dict['name']
        if user_platform_str == "":
            user_platform_str = user_platform_id
        row_lst = [
            user_log_time,
            user_uid,
            user_add_rmb,
            user_order_id,
            user_first_cost,
            user_ser_str,
            user_platform_str,
        ]

        temp_dict.setdefault(user_uid, []).append(row_lst)

    # 输出对应事件的文件
    out_put_file = open(out_put_path + "RECHARGE_LST", 'w')
    print out_put_file
    cPickle.dump(temp_dict, out_put_file)
    out_put_file.close()
    # time.sleep(1)
    end_time = time.time() - start_time
    print "file out time is :", end_time, "\n\n"




# start(['2015-06-05', '2015-06-05'])

def _get_server_list():
    """
        获取游戏服务器列表
    :rtype : object
    """
    from mysql import server_list
    all_server_list = server_list.get_all_server(True)

    return_ser_lst = []
    for item in all_server_list:
        server_id = item['id']
        server_name = item['name'] + '_' + str(item['id'])
        server_dict = {'id': server_id, 'name': server_name}
        return_ser_lst.append(server_dict)

    platform_list = [
        {'id': -1, 'name': u'通平台'},
        {'id': 0, 'name': u'测试'},
        {'id': 800003, 'name': u'海马'},
        {'id': 800004, 'name': u'飞流'},
        # {'id': 2, 'name': u'anysdk'},
        {'id': 500001, 'name':  u'iOS-91手机助手'},
        {'id': 500004, 'name':  u'iOS-iTools'},
        {'id': 500015, 'name':  u'iOS-快用'},
        {'id': 500017, 'name':  u'iOS-海马助手'},
        {'id': 500020, 'name':  u'iOS-爱思助手'},
        {'id': 500030, 'name':  u'iOS-XY助手'},
        {'id': 500002, 'name':  u'同步推'},
        {'id': 500003, 'name':  u'pp助手'},
        {'id': 800006, 'name':  u'爱苹果'},
        {'id': 500035, 'name':  u'叉叉助手'}
    ]
    return return_ser_lst, platform_list


if __name__ == '__main__':
    if len(sys.argv) > 1:
        split_date_str = sys.argv[1]
        split_date = datetime.datetime.strptime(split_date_str, "%Y-%m-%d").date()
        start_parse(split_date)
    else:
        split_date = datetime.date.today() - datetime.timedelta(days=1)
        start_parse(split_date)