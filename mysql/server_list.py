# -*- coding: utf-8 -*-

"""
游戏服务器地址
1.记录所有游戏服务器状态
2.所有游戏的登录服务器列表从此获取
create table server_list(
        id int not null primary key,
        url char(100) not null,
        name char(50) not null,
        state int not null,
        open_server__time datetime not null default '2015-01-01 00:00:00',
        hidden bool not null,
        send_player_trial_dat bool not null default False,
        send_player_sum_recharge_dat bool not null default False,
        send_player_daily_recharge_dat bool not null default False,
        send_stone_shop_dat bool not null default False,
        send_player_newbie bool not null default False,
        send_player_stage_detail bool not null default False,
        send_world_boss_dat bool not null default False,
        equip_dat bool not null default False,
        send_ditto_shop_dat bool not null default False,
        send_fragment_compound_dat bool not null default False,
        send_player_invition_dat bool not null default False,
        send_draw_dat bool not null default False,
        send_limit_exchange bool not null default False
        send_login_7 bool not null default False
        send_catch_monster bool not null default False
        send_player_sign_30 bool not null default False

    );
    Alter table server_list add column send_player_sign_30  bool not null default False
    show columns from server_world_boss;
    Alter table server_list add column open_server__time datetime not null default '2015-01-01 00:00:00'

"""
import datetime
import mysql_connection

TIME_DIS = 60  # 1 分钟查询一次

class _ServerListDat(object):
    """
        服务器数据
    """
    def __init__(self):
        super(_ServerListDat, self).__init__()
        self.cur_server_dat = None
        self.cur_all_server_dat = None
        self.cur_refresh_time = None

    def get_server_dat(self):
        """
            获取服务器数据
        """
        return self.cur_server_dat

    def get_refresh_time(self):
        """
            获取刷新时间
        """
        return self.cur_refresh_time

    def is_need_refresh(self):
        if self.cur_refresh_time:
            now = datetime.datetime.now()
            dis = now - self.cur_refresh_time
            if dis.seconds > TIME_DIS:
                return True
            return False
        else:
            return True

ServerListDat = _ServerListDat()

def get_all_server(refresh=False):
    """
        获取当前服务器列表
    """
    if ServerListDat.is_need_refresh() or refresh:
        connect = mysql_connection.get_game_manager_mysql_connection()
        ServerListDat.cur_all_server_dat = connect.query("SELECT * FROM server_list")
        ServerListDat.cur_refresh_time = datetime.datetime.now()
        return ServerListDat.cur_all_server_dat
    else:
        return ServerListDat.cur_all_server_dat


def get_server(server_id):
    """
        获取服务器
    """
    cur_ser = mysql_connection.get_game_manager_mysql_connection().query("SELECT * FROM server_list WHERE id = %s" % server_id)
    if cur_ser:
        return cur_ser[0]
    else:
        return None


def get_all_server_dict(refresh=False):
    """
        获取当前所有服务器的ID与网络地址的字典
    """
    if ServerListDat.is_need_refresh() or refresh:
        connect = mysql_connection.get_game_manager_mysql_connection()
        result_dict = {}
        server_dict = connect.query("SELECT id,url FROM server_list")
        for res in server_dict:
            result_dict[int(res['id'])] = res['url']
    return result_dict


def get_server_list_dat():
    """
        获取游戏服务器列表
  """

    get_all_server()
    server_list = []
    for item in ServerListDat.cur_all_server_dat:
        server_id = item['id']
        server_name = item['name'] + '_' + str(item['id'])
        server_dict = {'id': server_id, 'name': server_name}
        server_list.append(server_dict)
    return server_list

def update_server(server_id, url, name, state, hidden, version,open_server_time):
    """
        更新新服务器
    """
    sql = "SELECT * FROM server_list WHERE id = %s " %server_id
    dat = mysql_connection.get_game_manager_mysql_connection().query(sql)
    # print("dat: "+str(dat)+"notice: "+str(notice)+"version: "+str(version))
    if dat:
        sql = "UPDATE server_list SET " \
          "id = %s, " \
          "url = '%s', " \
          "name = '%s', " \
          "state = %s, " \
          "hidden = %s, " \
          "version = '%s', " \
          "open_server_time = '%s' " \
          "WHERE id = %s" %\
          (server_id, url, name, state, hidden, version, open_server_time, server_id)
        mysql_connection.get_game_manager_mysql_connection().execute(sql)
    else:
        sql = "INSERT INTO server_list (id,url,name,state,hidden,version,open_server_time) VALUES (%s,'%s','%s',%s,%s,'%s','%s')" % (server_id, url, name, state, hidden,version,open_server_time)
        mysql_connection.get_game_manager_mysql_connection().execute(sql)

def delete_server(server_id):
    """
        移除表格
    """
    sql = "DELETE FROM server_list WHERE id=%s" % server_id
    mysql_connection.get_game_manager_mysql_connection().execute(sql)