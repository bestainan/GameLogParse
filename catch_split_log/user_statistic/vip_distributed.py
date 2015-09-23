# -*- coding:utf-8 -*-

"""
    固定每天抓取拆分日志到当前服务器
    要伴随服务器开启而开启
"""
import pickle
import datetime
import sys
import os
import stat
from action.parse_action import log_parse
from util import game_define
from util.logs_out_path_of_parse import get_parse_path

CUR_ACTION_LST = [game_define.EVENT_ACTION_RECHARGE_PLAYER]     # 当前行为ID列表
cur_action_log_dict = dict()

# 当天所有新安装的用户
users_new_install_set = set()
users_new_install_num = 0
# 所有活跃用户（当天登录的非新玩家）
# user_active_set = set()
# user_active_num = 0

def start(split_date):
    """
        获取并拆分一天的日志
    """
    LOCAL_LOG_PATH_NAME_LST,OUT_PUT_PATH_LST = get_parse_path(split_date)
    # 本地打开
    for _server_id in LOCAL_LOG_PATH_NAME_LST:
        try:
            read_file = LOCAL_LOG_PATH_NAME_LST[_server_id].format(cur_date=split_date)
            log_lines = open(read_file, 'r')
            print(read_file)

            if log_lines:
                global users_new_install_set
                for _log_line in log_lines:
                    _log_line = _log_line.strip()
                    log_dict = log_parse(_log_line)
                    if not log_dict:
                        continue

                    action_id = log_dict['action']
                    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(action_id, 'Err')

                    # 插入活跃用户
                    if log_dict['install'] == split_date:
                        users_new_install_set.add(log_dict['uid'])

                    if log_dict['action'] in CUR_ACTION_LST:
                        # 插入列表 用来输出文件
                        if action_str in cur_action_log_dict:
                            cur_action_log_dict[action_str].append(log_dict)
                        else:
                            cur_action_log_dict[action_str] = [log_dict]
                _calculate_global()

                out_put_file_path = OUT_PUT_PATH_LST[_server_id].format(cur_date=split_date, use_path="tables")
                if not os.path.exists(out_put_file_path):
                    os.makedirs(out_put_file_path)
                os.chmod(out_put_file_path, stat.S_IRWXG + stat.S_IRWXO + stat.S_IRWXU)

                _output_VIP_DISTRIBUTED(out_put_file_path, split_date)
        except:
            pass


def _calculate_global():
    """
        全局数据计算
    """
    #计算活跃玩家数量
    # global user_active_num
    # global user_active_set
    # user_active_num = len(user_active_set)

    global users_new_install_num
    global users_new_install_set
    users_new_install_num = len(users_new_install_set)


def _output_VIP_DISTRIBUTED(out_put_file_path, split_date):
    """
        用户VIP分布
        条件	首冲	月卡	vip0	vip1	vip2	vip3	vip4	vip5	vip6	vip7	vip8	vip9	vip10	vip11	vip12
    """
    print("VIP_DISTRIBUTED")
    # global user_detail_dict
    global users_new_install_num

    action_str = game_define.EVENT_LOG_ACTION_SQL_NAME_DICT.get(game_define.EVENT_ACTION_RECHARGE_PLAYER, 'Err')
    recharge_logs = cur_action_log_dict.get(action_str, [])

    out_put_file = open(out_put_file_path + 'USER_DETAIL', 'r')
    _user_detail_dict = pickle.load(out_put_file)
    out_put_file.close()

    # _user_detail_dict = user_detail_dict
    _install_num = users_new_install_num

    # print len([dat['install'] for dat in _user_detail_dict.values() if dat['vip_level'] == 0])
    # print len([dat['install'] for dat in _user_detail_dict.values() if dat['vip_level'] == 0 and dat['install'] == split_date])
    # 首冲
    first_recharge = len(set([log['uid'] for log in recharge_logs if log['old_rmb'] == 0]))
    # 月卡
    month_card_recharge = len(set([log['uid'] for log in recharge_logs if log['shop_index'] == 1]))
    # vip总体登录
    total_line = ['总体登录', first_recharge, month_card_recharge]

    # 不带注册
    # for _vip_lv in xrange(13):
    #     user_num = len([dat['uid'] for dat in _user_detail_dict.values() if dat['vip_level'] == _vip_lv])
    #     total_line.append(user_num)
    # print _user_detail_dict.values()

    # 注册时间VIP分布
    total_line_dict = dict()
    total_line_dict['Total'] = [0] * 13
    for item in _user_detail_dict.values():
        install = item['install'].strftime('%Y-%m-%d')
        if install not in total_line_dict.keys():
            total_line_dict[install] = [0] * 13
            total_line_dict[install][item['vip_level']] += 1
            total_line_dict['Total'][item['vip_level']] += 1
        else:
            total_line_dict[install][item['vip_level']] += 1
            total_line_dict['Total'][item['vip_level']] += 1
    total_line_dict['cur_date'] = split_date
    # print "total_line_dict:"
    # print total_line_dict

    #------------ 新增部分---------
    add_line = ['新增角色数']
    add_line.extend([_install_num] * 15)

    # 首冲
    first_recharge = len(set([log['uid'] for log in recharge_logs if log['old_rmb'] == 0 and log['install'] == split_date]))
    # 月卡
    month_card_recharge = len(set([log['uid'] for log in recharge_logs if log['shop_index'] == 1 and log['install'] == split_date]))
    # vip 新增充值
    new_user_line = ['新增充值', first_recharge, month_card_recharge]

    for _vip_lv in xrange(13):
        new_user_num = len([dat['uid'] for dat in _user_detail_dict.values() if dat['vip_level'] == _vip_lv and dat['install'] == split_date])
        new_user_line.append(new_user_num)

    rate_line = ['比率']

    for _index in xrange(1, 16):
        rate = division(new_user_line[_index], add_line[_index])
        rate_line.append(str(rate*100)+'%')

    result = [
        total_line,
        new_user_line,
        add_line,
        rate_line,
        total_line_dict,
    ]
    # print "result:"
    # print result
    # 输出VIP 分布
    out_put_file = open(out_put_file_path + 'VIP_DISTRIBUTED', 'w')
    pickle.dump(result, out_put_file)
    out_put_file.close()


def division(num_1, num2):
    if not num2:
        return 0
    return round(float(num_1)/float(num2), 2)


if __name__ == "__main__":
    start(sys.argv)
