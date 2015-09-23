#coding:utf-8
from util import dat_log_util

def make_action_file(search_date, server_id):

    new_log_lst = dat_log_util.read_one_day_data("USER_DETAIL",search_date,'tables',server_id)

    print len(new_log_lst)

    # user_num_dict = dict()
    # lost_user_num_dict = dict()
    # for dat in new_log_lst.values():
    #     cur_lv = dat['level']
    #     if search_start_date == dat['install']:
    #         user_num_dict[cur_lv] = user_num_dict.get(cur_lv, 0) + 1
    #     #这里再查第二天的new_log_lst
    #     if search_start_date == dat['install'] and dat['last_play_time'].date() == dat['install']:
    #         lost_user_num_dict[cur_lv] = lost_user_num_dict.get(cur_lv, 0) + 1
    #
    # num_total = 0
    # for _table_lv in xrange(1, 121):
    #     num_total += user_num_dict.get(_table_lv, 0)
    #
    # # 遍历全部等级
    # table_row_lst = []
    # for _table_lv in xrange(1, 121):
    #     # 停留人数
    #     user_num = user_num_dict.get(_table_lv, 0)
    #     # 流失人数
    #     lost_num = lost_user_num_dict.get(int(_table_lv), 0)
    #
    #     # 留存人数
    #     stand_num = user_num - lost_num
    #
    #     # 等级比率
    #     level_rate = str(_get_rate(user_num, num_total)* 100) + "%"
    #     # 留存人数比率
    #     level_lost_rate = str(_get_rate(stand_num , num_total) * 100) + "%"
    #     #todo:
    #     # if _t
    #     # 等级	停留人数	留存人数比率	等级流存率
    #     content = [_table_lv, user_num, level_rate, level_lost_rate]
    #     table_row_lst.append(content)
    #
    # return table_row_lst

if  __name__ == '__main__':
    make_action_file('2015-07-18',10006)