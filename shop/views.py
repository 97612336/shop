import logging

from django.shortcuts import render

# 返回所有商品首页信息
from shop.utils import get_all_kind_goods, get_pages


def get_all_goods(request):
    page = int(request.GET.get('page', 1))
    goods_list, total_num = get_all_kind_goods(page)
    pages_dict = get_pages(total_num, page)
    context = {
        "goods_list": goods_list,
        "page_dict": pages_dict
    }
    return render(request, 'goods/goods_index.html', context=context)
