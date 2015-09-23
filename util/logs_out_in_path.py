# -*- coding:utf-8 -*-

#输入日志文件路径
OUT_PUT_PATH_LST = {
    10003:"/home/ubuntu/data/HaiMaLogParse/10003/",
    10004:"/home/ubuntu/data/HaiMaLogParse/10004/",
    10005:"/home/ubuntu/data/HaiMaLogParse/10005/",
    30001:"/home/ubuntu/data/HaiMaLogParse/30001/",
}
#解析总目录日志文件路径
LOCAL_LOG_PATH_NAME_LST = {
    10003:"/home/ubuntu/data/HaiMaLogs/10003_{cur_date}/10003_{cur_date}_00000",
    10004:"/home/ubuntu/data/HaiMaLogs/10004_{cur_date}/10004_{cur_date}_00000",
    10005:"/home/ubuntu/data/HaiMaLogs/10005_{cur_date}/10005_{cur_date}_00000",
    30001:"/home/ubuntu/data/HaiMaLogs/30001_{cur_date}/30001_{cur_date}_00000",
}
#获取日志文件路径
#cur == 日期
#use == 使用的文件目录 比如 UID_ACTION 或者 tables
CATCH_LOGS_DAT_LST ={
    10003:'/home/ubuntu/data/HaiMaLogParse/10003/{cur_date}/{use_path}/',
    10004:'/home/ubuntu/data/HaiMaLogParse/10004/{cur_date}/{use_path}/',
    10005:'/home/ubuntu/data/HaiMaLogParse/10005/{cur_date}/{use_path}/',
    30001:'/home/ubuntu/data/HaiMaLogParse/30001/{cur_date}/{use_path}/',
    -1:'/home/ubuntu/data/HaiMaLogParse/10005/{cur_date}/{use_path}/',
}
#在日志服上抓取当天日志文件路径
#cur == 日期
#use == 使用的文件目录 比如 UID_ACTION 或者 tables
HAIMA_LOG_SERVER = "http://115.159.69.65:8086/"
CATCH_TODAY_LOGS_DAT_LST = {
    10003: HAIMA_LOG_SERVER+'10003_{cur_date}/10003_{cur_date}_00000',
    10004: HAIMA_LOG_SERVER+'10004_{cur_date}/10004_{cur_date}_00000',
    10005: HAIMA_LOG_SERVER+'10005_{cur_date}/10005_{cur_date}_00000',
    30001: HAIMA_LOG_SERVER+'30001_{cur_date}/30001_{cur_date}_00000',
}

LOG_PATH="/home/ubuntu/data/HaiMaLogParse/logs_check/"