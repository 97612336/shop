import json
import logging
import math

import requests

from shop.settings import APP_KEY


# 获取所有商品信息
def get_all_kind_goods(page):
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
