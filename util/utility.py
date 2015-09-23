#coding: utf-8
"""
    公共函数
"""
import cPickle
import time
# from collections import deque
# queue = deque([1, 2, 3, 4])
# queue.append(5)
# print queue.popleft()
# print(queue)

READ_LINES = 200000
global_log_lst = []

# ------------------------file_last_line_num---------------------
def read_file_last_line(file_name):
    with open(file_name, 'r') as fh:
        count = 0

        while True:
            buffer = fh.read(1024 * 8192)

            if not buffer:
                break
            count += buffer.count('\n')
        fh.close()

        return count

# ------------------------trigger---------------------
def read_limit(dump_file_path, last_line_num, cur_read_line_num):
    # TOD:1.限制读取条数
    global global_log_lst
    if len(global_log_lst) >= READ_LINES:
        # print "READ_LINES...... "
        dump_loop_file(global_log_lst, dump_file_path)  # 到达限制数量dump一次
        global_log_lst = []

    elif len(global_log_lst) > 0 and last_line_num == cur_read_line_num:
        print "last dump_loop_file......   last_line is: ", cur_read_line_num
        dump_loop_file(global_log_lst, dump_file_path)  # 最后一次dump
        global_log_lst = []

# ------------------------loop_dump---------------------
def dump_loop_file(cur_log_dict_lst, dump_file_path):
    """
        循环dump
    """
    # dump到每个打开w+模式文件下
    cPickle.dump(cur_log_dict_lst, dump_file_path)

# ------------------------loop_load---once_dump---------------------
def loop_load_and_once_dump(loop_load_file_path):
    print 'this is once_dump '
    start_time = time.time()
    loop_load_file_path.seek(0)
    result_loop_lst_values = []     # 返回结果

    # 循环load # 每一次[[],[]]
    result_loop_lst_values = loop_load(loop_load_file_path)
    # 到头
    loop_load_file_path.seek(0)
    # once_dump
    cPickle.dump(result_loop_lst_values, loop_load_file_path)
    print(loop_load_file_path)
    # 关闭文件
    loop_load_file_path.close()

    end_time = time.time() - start_time
    print "cPickle once_dump all uid file time is: ", end_time


# ------------------------loop_load 打开的文件-----------------------
def loop_load(open_file):
    result = []
    while True:
        try:
            result.extend(cPickle.load(open_file))
        except:
            break

    return result

