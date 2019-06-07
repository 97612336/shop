import json
import logging
import math

import requests

from shop.settings import APP_KEY, TKZS_SESSION, PID, reset_tkzs_session, write_except


# 获取所有商品信息
def get_all_kind_goods(page, kind):
    if kind:

        if kind == 100:
            url = 'https://api.taokezhushou.com/api/v1/top_day'
            params = {
                "app_key": APP_KEY,
                'page': int(page),
            }
        else:
            url = "https://api.taokezhushou.com/api/v1/search"
            params = {
                "app_key": APP_KEY,
                'page': int(page),
                "cate_id": kind,
            }
    else:
        url = 'https://api.taokezhushou.com/api/v1/all'
        params = {
            "app_key": APP_KEY,
            'page': int(page)
        }
    res = requests.get(url=url, params=params)
    res_text = res.text
    res_json = json.loads(res_text)
    # 获取总的商品数量
    total_num = res_json.get('total')
    # 获取总的商品信息，一页一百个
    goods_data = res_json.get('data')
    return goods_data, total_num


# 获取分页的数字
def get_pages(total, curremt_page):
    tmp = {}
    page_size = 100
    # 总分页数
    max_page = math.ceil(total / page_size)
    logging.warning(max_page)
    all_page_list = [x + 1 for x in range(max_page)]
    curremt_page_index = all_page_list.index(curremt_page)
    # 获取分页列表
    if curremt_page in all_page_list[0:9]:
        page_list = all_page_list[0:9]
    elif curremt_page in all_page_list[-9:]:
        page_list = all_page_list[-9:]
    else:
        page_list = all_page_list[curremt_page_index - 4:curremt_page_index + 5]
    tmp['page_list'] = page_list
    # 获取下一页和上一页的相关信息
    if curremt_page == 1:
        tmp['has_per'] = 0
        tmp['per_num'] = 0
    else:
        tmp['has_per'] = 1
        tmp['per_num'] = curremt_page - 1
    if curremt_page == all_page_list[-1]:
        tmp['has_next'] = 0
        tmp['next_num'] = 0
    else:
        tmp['has_next'] = 1
        tmp['next_num'] = curremt_page + 1
    tmp['current_page'] = curremt_page
    return tmp


# 获取商品分类下的信息
def get_one_kind_goods(page, kind):
    url = 'https://api.taokezhushou.com/api/v1/search'
    params = {
        "app_key": APP_KEY,
        'page': int(page)
    }
    res = requests.get(url, params=params)
    res_text = res.text
    res_json = json.loads(res_text)
    # 获取总的商品数量
    total_num = res_json.get('total')
    # 获取总的商品信息，一页一百个
    goods_data = res_json.get('data')
    return goods_data, total_num


# 搜索商品
def util_search_goods(page, words, order):
    url = 'https://api.taokezhushou.com/api/v1/search'
    if order == 1:
        params = {
            "app_key": APP_KEY,
            "q": words,
            "page": int(page),
            "sort": "price_asc"
        }
    elif order == 2:
        params = {
            "app_key": APP_KEY,
            "q": words,
            "page": int(page),
            "sort": "price_desc"
        }
    elif order == 3:
        params = {
            "app_key": APP_KEY,
            "q": words,
            "page": int(page),
            "sort": "sale_num"
        }
    else:
        params = {
            "app_key": APP_KEY,
            "q": words,
            "page": int(page)
        }
    logging.warning(params)
    res = requests.get(url, params=params)
    res_text = res.text
    res_json = json.loads(res_text)
    # 获取总的商品数量
    total_num = res_json.get('total')
    # 获取总的商品信息，一页一百个
    goods_data = res_json.get('data')
    return goods_data, total_num


# 进入商品详情
def util_goods_detail(goods_id):
    url = 'https://api.taokezhushou.com/api/v1/detail'
    params = {
        "app_key": APP_KEY,
        "goods_id": goods_id
    }
    res = requests.get(url, params=params)
    res_text = res.text
    res_json = json.loads(res_text)
    goods_data = res_json.get('data')
    return goods_data


# 获取商品优惠券
def util_get_yhq(goods_id, coupon_id, short_title, def_run_num=0):
    cookies_dict = TKZS_SESSION.cookies.get_dict()
    url = 'http://www.taokezhushou.com/zhuanlian'
    data = {
        "goods_id": goods_id,
        "coupon_id": coupon_id,
        'text': short_title,
        'pid': PID,
        'resp': 'td'
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Mobile Safari/537.36",
    }
    res = requests.post(url=url, data=data, cookies=cookies_dict, headers=headers)
    # 错误处理
    try:
        res_dict = json.loads(res.text)
    except Exception as e:
        write_except(e)
        reset_tkzs_session(TKZS_SESSION)
        res = requests.post(url=url, data=data, cookies=cookies_dict, headers=headers)
        res_dict = json.loads(res.text)
    logging.warning(res_dict)
    if res_dict.get('status') == 200:
        yhq_dict = res_dict.get('data')
        return yhq_dict
    else:
        # 限制递归次数
        if def_run_num < 3:
            def_run_num = def_run_num + 1
            reset_tkzs_session(TKZS_SESSION)
            util_get_yhq(goods_id, coupon_id, short_title, def_run_num=def_run_num)
        else:
            return {}
