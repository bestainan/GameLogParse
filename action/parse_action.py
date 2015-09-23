# -*- coding:utf-8 -*-

from action import action_base
from action import action_create_role
from action import action_role_login
from action import action_get_guide
from action import action_role_level_up
from action import action_stone_shop
from action import action_ditto_shop
from action import action_pvp_shop
from action import action_world_boss_shop
from action import action_gym_shop
from action import action_arena_win
from action import action_arena_fail
from action import action_recharge_player
from action import action_stage_normal_fail
from action import action_stage_normal_win
from action import action_draw_one
from action import action_draw_ten
from action import action_treasure_level_up
from action import action_treasure_phase_up
from action import action_activity_seven_level
from action import action_activity_seven_power
from action import action_combat_power_error
from action import action_finger_guess_exchange
from action import action_equip_level_up_one
from action import action_equip_level_up_multi
from action import action_monster_advance
from action import action_monster_level_up
from action import action_monster_reset_individual_normal
from action import action_monster_skill_upgrade
from action import action_monster_upgrade_star
from action import action_advance_title
from action import action_world_boss_gold_inspire
from action import action_buy_miao_bank
from action import action_buy_gold
from action import action_buy_stamina
from action import action_buy_storage_num
from action import action_modify_name
from action import action_catch_monster
from action import action_chat
from action import action_ditto_shop_stone_reset
from action import action_gym_shop_stone_reset
from action import action_monster_rebirth
from action import action_monster_reset_individual_count
from action import action_monster_reset_individual_super
from action import action_arena_buy_challenge_count
from action import action_pvp_shop_stone_reset
from action import action_world_boss_reset_challenge_count
from action import action_world_boss_stone_inspire
from action import action_world_boss_shop_stone_reset
from action import action_buy_stage_count
from action import action_stone_shop_stone_reset
from action import action_get_level_gift
from action import action_daily_reward_stone
from action import action_month_card
from action import action_team_power_reward
from action import action_system_mail_reward
from action import action_miao_bank_reward
from action import action_monster_kind_reward
from action import action_monster_level_reward
from action import action_monster_quality_reward
from action import action_monster_star_level_reward
from action import action_daily_task_score_reward
from action import action_daily_task_task_reward
from action import action_exchange_gift
from action import action_fishing_loop
from action import action_fishing_once
from action import action_change_name_reward
from action import action_gym_reward
from action import action_login_7_reward
from action import action_i_invite_reward
from action import action_invite_me_reward
from action import action_recharge_daily_reward
from action import action_finish_newbie
from action import action_recharge_sum_reward
from action import action_sign_30_reward
from action import action_zone_gold_crown_reward
from action import action_zone_pass_reward
from action import action_lottery_reward
from action import action_vip_daily_reward
from action import action_arena_title_daily_reward
from action import action_battle_stage_mop
from action import action_equip_sell
from action import action_equip_exchange
from action import action_sun_stone_exchange
from action import action_gym_win
from action import action_gym_fail
from action import action_gym_mop
from action import action_gym_reset
from action import action_item_sell
from action import action_item_metal_gold_exchange_ditto
from action import action_compound_monster
from action import action_compound_equipment
from action import action_daily_reward_gold
from action import action_login_series_reward
from action import action_monster_evolute
from action import action_monster_free
from action import action_quiz_answer_true
from action import action_recharge_first_gift
from action import action_limit_time_exchange_monster
from action import action_sign_30_series_reward
from action import action_get_tonic
from action import action_treasure_battle_win
from action import action_treasure_battle_fail
from action import action_treasure_compose
from action import action_vip_level_gift
from action import action_world_boss_attack
from action import action_trial_battle_win
from action import action_trial_battle_fail
from action import action_exp_stage_buy_count
from action import action_gold_stage_buy_count
from action import action_pikachu_massage
from action import action_treasure_count_reset
from action import action_recharge_inner
from action import action_stage_hero_win
from action import action_stage_exp_win
from action import action_stage_gold_win
from action import action_stage_hero_fail
from action import action_stage_exp_fail
from action import action_stage_gold_fail
from action import action_activity_arena
from action import action_activity_finger_guess
from action import action_activity_fishing
from action import action_activity_gym
from action import action_activity_hard_stage
from action import action_activity_normal_stage
from action import action_activity_one_recharge
from action import action_activity_recharge_long
from action import action_activity_recharge_short
from action import action_activity_regist_recharge
from action import action_activity_treasure
from action import action_activity_weixin_share

from action import action_history_buddy_max_reward
from action import action_buddy_apply_player
from action import action_buddy_add_player
from action import action_buddy_remove_player
from action import action_buddy_refuse_player
from action import action_buddy_send_stamina
from action import action_buddy_receive_stamina
from action import action_buddy_receive_stamina_all
from action import action_buddy_contact
from action import action_buddy_contact_progress
from action import action_buddy_send_mail
from action import action_activity_holiday_shop
from action import action_activity_time_limited_shop
from action import action_activity_time_limited_shift_shop
from action import action_union_chat
from action import action_activity_stone_consumption
from action import action_fragment_shop

from action import action_union_shop
from action import action_union_shop_stone_reset
from action import action_union_apply_join
from action import action_union_accept_add_member
from action import action_union_create
from action import action_union_dismiss
from action import action_union_kick_member
from action import action_union_exit
from action import action_union_set_leader
from action import action_union_buy_reward
from action import action_union_sign
from action import action_union_stage_buy_count
from action import action_union_attack_stage
from action import action_union_pass_stage_reward_point
from action import action_union_pass_stage_chest
from action import action_union_sign_reward

from action import action_trial_essense_win
from action import action_trial_essense_fail
from action import action_chest_open

# 事件映射 解析用
from util import game_define

all_action_dict = {

    game_define.EVENT_ACTION_CREATE_ROLE: action_create_role,
    game_define.EVENT_ACTION_ROLE_LOGIN: action_role_login,
    game_define.EVENT_ACTION_FINISH_GUIDE: action_get_guide,
    game_define.EVENT_ACTION_ROLE_LEVEL_UP: action_role_level_up,
    game_define.EVENT_ACTION_STONE_SHOP_BUY: action_stone_shop,

    game_define.EVENT_ACTION_DITTO_SHOP_BUY: action_ditto_shop,
    game_define.EVENT_ACTION_PVP_SHOP_BUY: action_pvp_shop,
    game_define.EVENT_ACTION_WORLD_BOSS_SHOP_BUY: action_world_boss_shop,
    game_define.EVENT_ACTION_GYM_SHOP_BUY: action_gym_shop,
    game_define.EVENT_ACTION_COMBAT_POWER_ERROR: action_combat_power_error,
    game_define.EVENT_ACTION_ARENA_WIN: action_arena_win,
    game_define.EVENT_ACTION_ARENA_FAIL: action_arena_fail,
    game_define.EVENT_ACTION_ONE_DRAW: action_draw_one,
    game_define.EVENT_ACTION_TEN_DRAW: action_draw_ten,
    game_define.EVENT_ACTION_RECHARGE_PLAYER: action_recharge_player,
    game_define.EVENT_ACTION_RECHARGE_INNER: action_recharge_inner,
    game_define.EVENT_ACTION_STAGE_NORMAL_WIN: action_stage_normal_win,
    game_define.EVENT_ACTION_STAGE_NORMAL_FAIL: action_stage_normal_fail,
    game_define.EVENT_ACTION_TREASURE_LEVEL_UP: action_treasure_level_up,
    game_define.EVENT_ACTION_TREASURE_PHASE_UP: action_treasure_phase_up,
    game_define.EVENT_ACTION_ACTIVITY_SEVEN_LEVEL_REWARD: action_activity_seven_level,
    game_define.EVENT_ACTION_ACTIVITY_SEVEN_POWER_REWARD: action_activity_seven_power,

    game_define.EVENT_ACTION_FINGER_GUESS_EXCHANGE: action_finger_guess_exchange,
    game_define.EVENT_ACTION_EQUIP_LEVEL_UP: action_equip_level_up_one,
    game_define.EVENT_ACTION_EQUIP_LEVEL_UP_MULTI: action_equip_level_up_multi,
    game_define.EVENT_ACTION_ADVANCE_MONSTER: action_monster_advance,
    game_define.EVENT_ACTION_LEVEL_UP_MONSTER: action_monster_level_up,
    game_define.EVENT_ACTION_RESET_INDIVIDUAL_MONSTER: action_monster_reset_individual_normal,
    game_define.EVENT_ACTION_UPGRADE_MONSTER_SKILL: action_monster_skill_upgrade,
    game_define.EVENT_ACTION_UPDATE_STAR_MONSTER: action_monster_upgrade_star,
    game_define.EVENT_ACTION_ADVANCE_TITLE: action_advance_title,
    game_define.EVENT_ACTION_WB_GOLD_INSPIRE: action_world_boss_gold_inspire,
    game_define.EVENT_ACTION_BUY_MIAO_BANK: action_buy_miao_bank,
    game_define.EVENT_ACTION_BUY_GOLD: action_buy_gold,
    game_define.EVENT_ACTION_BUY_STAMINA: action_buy_stamina,
    game_define.EVENT_ACTION_BUY_STORAGENUM: action_buy_storage_num,
    game_define.EVENT_ACTION_MODIFY_NAME: action_modify_name,
    game_define.EVENT_ACTION_GET_CATCH_MONSTER_RESULT: action_catch_monster,
    game_define.EVENT_ACTION_CHAT: action_chat,
    game_define.EVENT_ACTION_STONE_RESET_DITTO_SHOP: action_ditto_shop_stone_reset,
    game_define.EVENT_ACTION_STONE_RESET_GYM_SHOP: action_gym_shop_stone_reset,
    game_define.EVENT_ACTION_MONSTER_REBIRTH: action_monster_rebirth,
    game_define.EVENT_ACTION_RESET_INDIVIDUAL_COUNT: action_monster_reset_individual_count,
    game_define.EVENT_ACTION_STONE_RESET_INDIVIDUAL_MONSTER: action_monster_reset_individual_super,
    game_define.EVENT_ACTION_ARENA_BUY_COUNT: action_arena_buy_challenge_count,
    game_define.EVENT_ACTION_STONE_RESET_PVP_SHOP: action_pvp_shop_stone_reset,
    game_define.EVENT_ACTION_WB_RESET_COUNT: action_world_boss_reset_challenge_count,
    game_define.EVENT_ACTION_WB_STONE_INSPIRE: action_world_boss_stone_inspire,
    game_define.EVENT_ACTION_STONE_RESET_WB_SHOP: action_world_boss_shop_stone_reset,
    game_define.EVENT_ACTION_BUY_STAGE_COUNT: action_buy_stage_count,
    game_define.EVENT_ACTION_STONE_RESET_STONE_SHOP: action_stone_shop_stone_reset,
    game_define.EVENT_ACTION_LEVEL_GIFT: action_get_level_gift,
    game_define.EVENT_ACTION_DAILY_REWARD_STONE: action_daily_reward_stone,
    game_define.EVENT_ACTION_MONTH_CARD: action_month_card,
    game_define.EVENT_ACTION_TEAM_POWER_REWARD: action_team_power_reward,
    game_define.EVENT_ACTION_GET_SYSTEM_MAIL_REWARD: action_system_mail_reward,
    game_define.EVENT_ACTION_GET_MIAOBANK_REWARD: action_miao_bank_reward,
    game_define.EVENT_ACTION_GET_MONSTER_KIND: action_monster_kind_reward,
    game_define.EVENT_ACTION_GET_MONSTER_LEVEL: action_monster_level_reward,
    game_define.EVENT_ACTION_GET_MONSTER_QUALITY: action_monster_quality_reward,
    game_define.EVENT_ACTION_GET_MONSTER_STAR_LEVEL: action_monster_star_level_reward,
    game_define.EVENT_ACTION_DAILY_TASK_SCORE_REWARD: action_daily_task_score_reward,
    game_define.EVENT_ACTION_DAILY_TASK_TASK_REWARD: action_daily_task_task_reward,
    game_define.EVENT_ACTION_EXCHANGE_GIFT: action_exchange_gift,
    game_define.EVENT_ACTION_FISHING_LOOP: action_fishing_loop,
    game_define.EVENT_ACTION_FISHING_ONCE: action_fishing_once,
    game_define.EVENT_ACTION_CHANGE_NAME: action_change_name_reward,
    game_define.EVENT_ACTION_GYM_REWARD: action_gym_reward,
    game_define.EVENT_ACTION_LOGIN_7_REWARD: action_login_7_reward,
    game_define.EVENT_ACTION_I_INVITE_REWARD: action_i_invite_reward,
    game_define.EVENT_ACTION_INVITE_ME_REWARD: action_invite_me_reward,
    game_define.EVENT_ACTION_DAILY_RECHARGE_REWARD: action_recharge_daily_reward,
    game_define.EVENT_ACTION_FINISH_NEWBIE: action_finish_newbie,
    game_define.EVENT_ACTION_SUM_RECHARGE_REWARD: action_recharge_sum_reward,
    game_define.EVENT_ACTION_SIGN_30: action_sign_30_reward,
    game_define.EVENT_ACTION_ZONE_GOLD_CROWN_REWARD: action_zone_gold_crown_reward,
    game_define.EVENT_ACTION_ZONE_PASS_REWARD: action_zone_pass_reward,
    game_define.EVENT_ACTION_LOTTERY_REWARD: action_lottery_reward,
    game_define.EVENT_ACTION_VIP_DAILY_REWARD: action_vip_daily_reward,
    game_define.EVENT_ACTION_ARENA_DAILY_REWARD: action_arena_title_daily_reward,
    game_define.EVENT_ACTION_STAGE_MOP: action_battle_stage_mop,
    game_define.EVENT_ACTION_EQUIP_SELL: action_equip_sell,
    game_define.EVENT_ACTION_EQUIP_EXCHANGE_GET_ITEMS: action_equip_exchange,
    game_define.EVENT_ACTION_SUN_STONE_EXCHANGE: action_sun_stone_exchange,
    game_define.EVENT_ACTION_GYM_WIN: action_gym_win,
    game_define.EVENT_ACTION_GYM_FAIL: action_gym_fail,
    game_define.EVENT_ACTION_GYM_MOP: action_gym_mop,
    game_define.EVENT_ACTION_GYM_RESET: action_gym_reset,
    game_define.EVENT_ACTION_SELL_ITEM: action_item_sell,
    game_define.EVENT_ACTION_EXCHANGE_MONSTER: action_item_metal_gold_exchange_ditto,
    game_define.EVENT_ACTION_COMPOUND_MONSTER: action_compound_monster,
    game_define.EVENT_ACTION_COMPOUND_EQUIP: action_compound_equipment,
    game_define.EVENT_ACTION_DAILY_REWARD_GOLD: action_daily_reward_gold,
    game_define.EVENT_ACTION_LOGIN_SERIES_REWARD: action_login_series_reward,
    game_define.EVENT_ACTION_EVOLUTE_MONSTER: action_monster_evolute,
    game_define.EVENT_ACTION_MONSTER_FREE: action_monster_free,
    game_define.EVENT_ACTION_QUIZ_ANSWER_TRUE: action_quiz_answer_true,
    game_define.EVENT_ACTION_GET_FIRST_RECHARGE_GIFT: action_recharge_first_gift,
    game_define.EVENT_ACTION_SHOP_EXCHANGE: action_limit_time_exchange_monster,
    game_define.EVENT_ACTION_SIGN_30_SERIES: action_sign_30_series_reward,
    game_define.EVENT_ACTION_GET_TONIC: action_get_tonic,
    game_define.EVENT_ACTION_TREASURE_BATTLE_WIN: action_treasure_battle_win,
    game_define.EVENT_ACTION_TREASURE_BATTLE_FAIL: action_treasure_battle_fail,
    game_define.EVENT_ACTION_TREASURE_COMPOSE: action_treasure_compose,
    game_define.EVENT_ACTION_VIP_LEVEL_GIFT: action_vip_level_gift,
    game_define.EVENT_ACTION_WORLD_BOSS_ATTACK: action_world_boss_attack,
    game_define.EVENT_ACTION_TRIAL_BATTLE_WIN: action_trial_battle_win,
    game_define.EVENT_ACTION_TRIAL_BATTLE_FAIL: action_trial_battle_fail,
    game_define.EVENT_ACTION_EXP_STAGE_BUY_COUNT: action_exp_stage_buy_count,
    game_define.EVENT_ACTION_GOLD_STAGE_BUY_COUNT: action_gold_stage_buy_count,
    game_define.EVENT_ACTION_MASSAGE_REWARD: action_pikachu_massage,
    game_define.EVENT_ACTION_TREASURE_COUNT_RESET: action_treasure_count_reset,
    game_define.EVENT_ACTION_STAGE_HERO_WIN: action_stage_hero_win,
    game_define.EVENT_ACTION_STAGE_EXP_WIN: action_stage_exp_win,
    game_define.EVENT_ACTION_STAGE_GOLD_WIN: action_stage_gold_win,
    game_define.EVENT_ACTION_STAGE_HERO_FAIL: action_stage_hero_fail,
    game_define.EVENT_ACTION_STAGE_EXP_FAIL: action_stage_exp_fail,
    game_define.EVENT_ACTION_STAGE_GOLD_FAIL: action_stage_gold_fail,
    game_define.EVENT_ACTION_ACTIVITY_ARENA_REWARD: action_activity_arena,
    game_define.EVENT_ACTION_ACTIVITY_FINGER_GUESS_REWARD: action_activity_finger_guess,
    game_define.EVENT_ACTION_ACTIVITY_FISHING_REWARD: action_activity_fishing,
    game_define.EVENT_ACTION_ACTIVITY_GYM_REWARD: action_activity_gym,
    game_define.EVENT_ACTION_ACTIVITY_HARD_STAGE_REWARD: action_activity_hard_stage,
    game_define.EVENT_ACTION_ACTIVITY_NORMAL_STAGE_REWARD: action_activity_normal_stage,
    game_define.EVENT_ACTION_ACTIVITY_ONE_RECHARGE: action_activity_one_recharge,
    game_define.EVENT_ACTION_ACTIVITY_RECHARGE_LONG: action_activity_recharge_long,
    game_define.EVENT_ACTION_ACTIVITY_RECHARGE_SHORT: action_activity_recharge_short,
    game_define.EVENT_ACTION_ACTIVITY_REGIST_RECHARGE: action_activity_regist_recharge,
    game_define.EVENT_ACTION_ACTIVITY_TREASURE_REWARD: action_activity_treasure,
    game_define.EVENT_ACTION_ACTIVITY_WEIXIN_SHARE: action_activity_weixin_share,
    #game_define.EVENT_ACTION_ACTIVITY_TIME_LIMITED_SHIFT_SHOP

    game_define.EVENT_ACTION_BUDDY_CONTACT: action_buddy_contact,
    game_define.EVENT_ACTION_REWARD_BUDDY_CONTACT: action_buddy_contact_progress,
    game_define.EVENT_ACTION_ACTIVITY_STONE_CONSUMPTION_REWARD: action_activity_stone_consumption,
    game_define.EVENT_ACTION_HISTORY_BUDDY_MAX_REWARD: action_history_buddy_max_reward,
    game_define.EVENT_ACTION_BUDDY_APPLY_PLAYER: action_buddy_apply_player,
    game_define.EVENT_ACTION_BUDDY_ADD_PLAYER: action_buddy_add_player,
    game_define.EVENT_ACTION_BUDDY_REMOVE_PLAYER: action_buddy_remove_player,
    game_define.EVENT_ACTION_BUDDY_REFUSE_PLAYER:  action_buddy_refuse_player,
    game_define.EVENT_ACTION_BUDDY_SEND_STAMINA: action_buddy_send_stamina,
    game_define.EVENT_ACTION_BUDDY_RECEIVE_STAMINA: action_buddy_receive_stamina,
    game_define.EVENT_ACTION_BUDDY_RECEIVE_STAMINA_ALL: action_buddy_receive_stamina_all,
    game_define.EVENT_ACTION_BUDDY_SEND_MAIL: action_buddy_send_mail,
    game_define.EVENT_ACTION_UNION_CHAT: action_union_chat,
    game_define.EVENT_ACTION_ACTIVITY_HOLIDAY_SHOP: action_activity_holiday_shop,
    game_define.EVENT_ACTION_ACTIVITY_TIME_LIMITED_SHOP: action_activity_time_limited_shop,
    game_define.EVENT_ACTION_ACTIVITY_TIME_LIMITED_SHIFT_SHOP: action_activity_time_limited_shift_shop,
    game_define.EVENT_ACTION_FRAGMENT_SHOP_BUY: action_fragment_shop,
    game_define.EVENT_ACTION_UNION_SHOP_BUY: action_union_shop,
    game_define.EVENT_ACTION_STONE_RESET_UNION_SHOP: action_union_shop_stone_reset,
    game_define.EVENT_ACTION_UNION_APPLY_JOIN: action_union_apply_join,
    game_define.EVENT_ACTION_UNION_ACCEPT_ADD_MEMBER: action_union_accept_add_member,
    game_define.EVENT_ACTION_UNION_CREATE: action_union_create,
    game_define.EVENT_ACTION_UNION_DISMISS: action_union_dismiss,
    game_define.EVENT_ACTION_UNION_KICK_MEMBER: action_union_kick_member,
    game_define.EVENT_ACTION_UNION_EXIT: action_union_exit,
    game_define.EVENT_ACTION_UNION_SET_LEADER: action_union_set_leader,
    game_define.EVENT_ACTION_UNION_BUY_REWARD: action_union_buy_reward,
    game_define.EVENT_ACTION_UNION_SIGN: action_union_sign,
    game_define.EVENT_ACTION_UNION_STAGE_BUY_COUNT: action_union_stage_buy_count,
    game_define.EVENT_ACTION_UNION_ATTACK_STAGE: action_union_attack_stage,
    game_define.EVENT_ACTION_UNION_PASS_STAGE_REWARD_POINT: action_union_pass_stage_reward_point,
    game_define.EVENT_ACTION_UNION_PASS_STAGE_CHEST: action_union_pass_stage_chest,
    game_define.EVENT_ACTION_UNION_SIGN_REWARD: action_union_sign_reward,
    game_define.EVENT_ACTION_TRIAL_ESSENSE_WIN: action_trial_essense_win,
    game_define.EVENT_ACTION_TRIAL_ESSENSE_FAIL: action_trial_essense_fail,
    game_define.EVENT_ACTION_CHEST_OPEN: action_chest_open,

}


def log_parse(log_dat):
    """
        解析日志行
    """
    try:
        result, log_lst = action_base.parse(log_dat)
        action = int(log_lst[0])
        action_val = all_action_dict[action]

        result.update(action_val.parse(log_lst))
        return result
    except:
        print("解析日志行出错:"+str(log_dat))
        return False


