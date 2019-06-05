import logging

from django.shortcuts import render

from shop.utils import get_all_kind_goods, get_pages, get_one_kind_goods, util_search_goods, util_goods_detail, \
    util_get_yhq


# # 返回所有商品首页信息，1女装 2男装 3内衣 4数码家电 5美食 6美妆个护 7母婴 8鞋包配饰 9家居家装 10文体车品 11其他
def get_all_goods(request):
    page = int(request.GET.get('page', 1))
    kind = int(request.GET.get('kind', 0))
    goods_list, total_num = get_all_kind_goods(page, kind)
    pages_dict = get_pages(total_num, page)
    context = {
        "goods_list": goods_list,
        "page_dict": pages_dict,
        "kind": kind
    }
    return render(request, 'goods/goods_index.html', context=context)


# 搜索商品
def search_goods(request):
    page = int(request.GET.get('page', 1))
    words = request.GET.get('words', '')
    order = int(request.GET.get('order', 0))
    goods_list, total_num = util_search_goods(page=page, words=words, order=order)
    pages_dict = get_pages(total_num, page)
    context = {
        "goods_list": goods_list,
        "page_dict": pages_dict,
        "order": order,
        "words": words
    }
    return render(request, 'goods/search_results.html', context=context)


# 点击进入商品详情
def goods_detail(request):
    goods_id = request.GET.get('goods_id')
    goods_detail = util_goods_detail(goods_id)
    coupon_id = goods_detail.get('coupon_id')
    short_title = goods_detail.get('goods_short_title')
    yhq = util_get_yhq(goods_id, coupon_id, short_title)
    context = {
        "goods_detail": goods_detail,
        "goods_id": goods_id,
        "yhq": yhq
    }
    return render(request, "goods/goods_detail.html", context=context)
