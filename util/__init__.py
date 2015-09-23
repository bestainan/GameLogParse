# -*- coding: utf-8 -*-
import math
import random
from util.mpycache import LRUCache as Cache

def generate_random_number_in_interval(ranges):
    """
        注意顺序
        contents.sort(key=lambda x: x['dropChance'])
        ranges 区间[100,200,300, 600] 当随机出来的数字为201的时候， 返回：1
        ranges 必须为最后一个数值为区间总的权重值
    """
    maxRand = max(ranges)
    if maxRand == 0:
        return -1, 0
    randint = random.randint(1, maxRand)

    index = None
    for index, value in enumerate(ranges):
        if randint <= value:
            break
    return index

def change_weight_in_interval(weights):
    """
        权重列表转换到区间列表
    """
    interval = [sum(weights[:index]) for index in range(1, len(weights) + 1)]
    return interval


class NotFound(object):
    pass #end class NotFound

class api_result_cache(object):
    """

    缓存调用结果
    {
    uid: {
        method: [(timeStamp, value)]
         }
    }
    
    """
    maxSize = 5000; # after pruning cache will come down to 10 elements
    maxAgeMillis = 60*1000*60*3; # 3 hours
    elasticity = 2000; # the cache will at most have 10+3=13 element
    cache = Cache(maxSize, maxAgeMillis, elasticity);


    
    @classmethod
    def get(cls, api_context):
        uid = api_context.rk_user.uid
        timestamp = api_context.get_parameter('timeStamp')
        method = api_context.get_parameter('method')

        values = cls.cache.get(uid, NotFound)
        if values == NotFound:
            return None

        method_result = values.get(method, NotFound)
        if method_result == NotFound:
            return None

        if method_result[0] == timestamp:
            return method_result[1]
        else:
            return None

        return value # end def get

    
    @classmethod
    def put(cls, api_context, value):
        if not value:
            return

        exclude_methods = ['user.GameInfo',]
        method = api_context.get_parameter('method')
        if method in exclude_methods or api_context.get_parameter('timeStamp', None) is None:
            return

        uid = api_context.rk_user.uid
        method = api_context.get_parameter('method')        
        timestamp = api_context.get_parameter('timeStamp')
        
        user_values = dict()
        user_values = cls.cache.get(uid, dict())
        user_values[method] = [timestamp, value]

        cls.cache.put(uid, user_values)

        return value # end def setup

    @classmethod
    def erase(cls, key):
        cls.cache.erase(key)
        return # end def erase
    pass #end class api_result_cache



def index_in_list(lst, fn):
    """
    在lst中查找会让fn返会为True的第一个元素，
    返会： 被命中元素的index， 该元素
    fn = lambda x: x==1
    index_in_list([0,1,2], fn) ==> 1, 1
    """

    index, element = None, None
    for index, element in enumerate(iter(lst)):
        if fn(element):
            break
        pass
    
    return index, element # end def find_in_list


def list_to_string(lst):
    """
        把列表转成字符串 [1,2,3] 转换 1,2,3
    """
    lst_str = map(lambda x: str(x), lst)
    return ','.join(lst_str)

def string_split_to_int_list(str,   sep=','):
    """
        字符串切割成int数组
    """
    if str == '' or None:
        return []
    lst_str = str.split(sep)
    lst_int = map(lambda x: int(x), lst_str)
    return lst_int

def user_random(user, a, b, random_type=None):
    """
        玩家随机数产生
    """
    # if random_type:
    #     random.seed(user.add_time)
    #     state = user.player_random_state.get_random_state(random_type)
    #     if state:
    #         # print("设置玩家随机种子 : " + str(user.add_time))
    #         # print("设置玩家随机状态 : " + str(state[0]))
    #         random.setstate(state)

    result = random.randint(a, b)

    # if random_type:
    #     user.player_random_state.set_random_state(random_type, random.getstate())
    #     user.player_random_state.put()
    #
    # random.seed(None)
    return result


def int10_to_int36(n):
    """
        10进制转换36进制
    """
    loop = '0123456789abcdefghijklmnopqrstuvwxyz'
    a = []
    while n != 0:
        a.append(loop[n % 36])
        n /= 36
    a.reverse()
    return ''.join(a)

def int36_to_int10(n):
    """
        转换36进制到10进制
    """
    try:
        return int(n, 36)
    except:
        return 0


def lst_choice_to_int(lst):
    """
        列表按位转换成int
    """
    result = 0
    for index, val in enumerate(lst):
        code = int(math.pow(2, index))
        if val:
            result |= code
    return result