# -*- coding:utf-8 -*-

from game_manager.action_gm import action_base_gm
from game_manager.action_gm import action_super_manager_register
from game_manager.action_gm import action_delete_manager
from game_manager.action_gm import action_manager_register
from game_manager.action_gm import action_manager_login
from game_manager.action_gm import action_update_password
from game_manager.action_gm import action_update_manager_info
from game_manager.action_gm import action_edit_player
from game_manager.action_gm import action_create_monster
from game_manager.action_gm import action_change_monster
from game_manager.action_gm import action_delete_monster
from game_manager.action_gm import action_add_item
from game_manager.action_gm import action_change_item
from game_manager.action_gm import action_delete_item
from game_manager.action_gm import action_add_equip
from game_manager.action_gm import action_change_equip
from game_manager.action_gm import action_delete_equip
from game_manager.action_gm import action_insert_server
from game_manager.action_gm import action_update_server
from game_manager.action_gm import action_delete_server
from game_manager.action_gm import action_insert_version_notice
from game_manager.action_gm import action_update_version_notice
from game_manager.action_gm import action_delete_version_notice
from game_manager.action_gm import action_insert_gift
from game_manager.action_gm import action_edit_gift
from game_manager.action_gm import action_update_notice
from game_manager.action_gm import action_delete_notice
from game_manager.action_gm import action_add_mail
from game_manager.action_gm import action_delete_mail
from game_manager.action_gm import action_add_bug_mail
from game_manager.action_gm import action_delete_bug
from game_manager.action_gm import action_delete_bug_all
from game_manager.action_gm import action_change_activity
from game_manager.action_gm import action_insert_exchange_code
from game_manager.action_gm import action_publish_config
from game_manager.action_gm import action_remove_config
from game_manager.action_gm import action_change_server_version
from game_manager.action_gm import action_change_server_config


# 事件映射 解析用
from util import game_define

all_action_dict = {

    game_define.GM_ACTION_SUPER_REGISTER: action_super_manager_register,
    game_define.GM_ACTION_DELETE_MANAGER: action_delete_manager,
    game_define.GM_ACTION_MANAGER_REGISTER: action_manager_register,
    game_define.GM_ACTION_MANAGER_LOGIN: action_manager_login,
    game_define.GM_ACTION_UPDATE_PASSWORD: action_update_password,
    game_define.GM_ACTION_UPDATE_MANAGER_INFO: action_update_manager_info,
    game_define.GM_ACTION_EDIT_PLAYER: action_edit_player,
    game_define.GM_ACTION_CREATE_MONSTER: action_create_monster,
    game_define.GM_ACTION_CHANGE_MONSTER: action_change_monster,
    game_define.GM_ACTION_DELETE_MONSTER: action_delete_monster,
    game_define.GM_ACTION_ADD_ITEM: action_add_item,
    game_define.GM_ACTION_CHANGE_ITEM: action_change_item,
    game_define.GM_ACTION_DELETE_ITEM: action_delete_item,
    game_define.GM_ACTION_ADD_EQUIP: action_add_equip,
    game_define.GM_ACTION_CHANGE_EQUIP: action_change_equip,
    game_define.GM_ACTION_DELETE_EQUIP: action_delete_equip,
    game_define.GM_ACTION_INSERT_SERVER: action_insert_server,
    game_define.GM_ACTION_UPDATE_SERVER: action_update_server,
    game_define.GM_ACTION_DELETE_SERVER: action_delete_server,
    game_define.GM_ACTION_INSERT_VERSION_NOTICE: action_insert_version_notice,
    game_define.GM_ACTION_UPDATE_VERSION_NOTICE: action_update_version_notice,
    game_define.GM_ACTION_DELETE_VERSION_NOTICE: action_delete_version_notice,
    game_define.GM_ACTION_INSERT_GIFT: action_insert_gift,
    game_define.GM_ACTION_EDIT_GIFT: action_edit_gift,
    game_define.GM_ACTION_UPDATE_NOTICE: action_update_notice,
    game_define.GM_ACTION_DELETE_NOTICE: action_delete_notice,
    game_define.GM_ACTION_ADD_MAIL: action_add_mail,
    game_define.GM_ACTION_DELETE_MAIL: action_delete_mail,
    game_define.GM_ACTION_ADD_BUG_MAIL: action_add_bug_mail,
    game_define.GM_ACTION_DELETE_BUG: action_delete_bug,
    game_define.GM_ACTION_DELETE_BUG_ALL: action_delete_bug_all,
    game_define.GM_ACTION_CHANGE_ACTIVITY: action_change_activity,
    game_define.GM_ACTION_INSERT_EXCHANGE_CODE: action_insert_exchange_code,
    game_define.GM_ACTION_PUBLISH_CONFIG: action_publish_config,
    game_define.GM_ACTION_REMOVE_CONFIG: action_remove_config,
    game_define.GM_ACTION_CHANGE_SERVER_VERSION: action_change_server_version,
    game_define.GM_ACTION_CHANGE_SERVER_CONFIG: action_change_server_config,


}


def gm_log_parse(log_dat):
    """
        解析日志行
    """
    try:
        result, log_lst = action_base_gm.parse(log_dat)
        action = int(log_lst[0])
        action_val = all_action_dict[action]

        result.update(action_val.parse(log_lst))
        return result
    except:
        return False


