from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import *
from django.core.paginator import Paginator
from df_cart.models import BrowseHistory
# Create your views here.

'''
显示首页
'''
# /goods/   显示首页
def home_list_page(request):
    '''返回首页'''
    # 1 查询每种商品的4个编号商品和3个最新商品
    fruits = Goods.objects.get_goods_by_type(goods_type_id=FRUIT,limit=4)
    fruits_new = Goods.objects.get_goods_by_type(goods_type_id=FRUIT,limit=3,order_by=('-create_time',) )
    seafood = Goods.objects.get_goods_by_type(goods_type_id=SEAFOOD, limit=4)
    seafood_new = Goods.objects.get_goods_by_type(goods_type_id=SEAFOOD, limit=3, order_by=('-create_time',))
    meat = Goods.objects.get_goods_by_type(goods_type_id=MEAT, limit=4)
    meat_new = Goods.objects.get_goods_by_type(goods_type_id=MEAT, limit=3, order_by=('-create_time',))
    eggs = Goods.objects.get_goods_by_type(goods_type_id=EGGS, limit=4)
    eggs_new = Goods.objects.get_goods_by_type(goods_type_id=EGGS, limit=3, order_by=('-create_time',))
    vegetables = Goods.objects.get_goods_by_type(goods_type_id=VEGETABLES, limit=4)
    vegetables_new = Goods.objects.get_goods_by_type(goods_type_id=VEGETABLES, limit=3, order_by=('-create_time',))
    frozen = Goods.objects.get_goods_by_type(goods_type_id=FROZEN, limit=4)
    frozen_new = Goods.objects.get_goods_by_type(goods_type_id=FROZEN, limit=3, order_by=('-create_time',))

    context = {
        'fruits':fruits,
        "fruits_new":fruits_new,
        'seafood':seafood,
        "seafood_new":seafood_new,
        'meat':meat,
        'meat_new':meat_new,
        'eggs':eggs,
        'eggs_new':eggs_new,
        'vegetables':vegetables,
        'vegetables_new':vegetables_new,
        'frozen':frozen,
        'frozen_new':frozen_new
    }

    # username = request.session.get('username',None)
    return render(request, 'df_goods/index.html',context)

# /goods/数字/    商品详情信息
def goods_detail(request,goods_id):
    '''商品详情信息'''
    goods = Goods.objects.get_goods_by_id(goods_id = goods_id)
    goods_new = Goods.objects.get_goods_by_type(goods_type_id=goods.goods_type_id,limit=2,order_by=('-create_time',))
    type_title = GOODS_TYPE[goods.goods_type_id]
    img = Image.objects.get_image_by_goods_id(goods_id)
    # 如果是登陆的用户 为该用户和该商品生成一条近期浏览记录
    if request.session.has_key('islogin'):
        passport_id = request.session.get('passport_id')
        BrowseHistory.objects.add_one_history(passport_id=passport_id,goods_id=goods_id)

    context = {
        'goods':goods,
        'goods_new':goods_new,
        'type_title':type_title,
        'goods_type_id':goods.goods_type_id,
        'img':img,
        'flag':'detail'
    }
    return render(request,'df_goods/detail.html',context)



# /list/种类id/页码/？sort=排序方式  商品列表页
def goods_list(request,goods_type_id,pindex):
    sort = request.GET.get('sort','default')
    if sort == 'default':
        sort = '-pk'
    elif sort == 'price':
        sort = 'goods_price'
    elif sort == 'hot':
        sort = '-goods_sales'
    goods_list = Goods.objects.get_ordered_object_list(filters={'goods_type_id':goods_type_id},order_by=(sort,))
    #对查询出来的商品进行分页操作
    paginator = Paginator(object_list=goods_list,per_page=1)
    pindex = int(pindex)
    goods_list = paginator.page(pindex) # 第pindex页数据
    nums = paginator.num_pages #分页之后的总页数
    #调整分页列表 最多显示5夜
    if nums<=5:
        pages = range(1,nums+1)
    elif pindex < 3:
        pages = range(1,6)
    elif nums-pindex <= 2 :
        pages = range(nums-4,nums+1)
    else :
        pages = range(pindex-2,pindex+3)

    #新品推荐 按照时间降序取两个
    goods_new_list = Goods.objects.get_goods_by_type(goods_type_id,limit=2,order_by=('-create_time', ))
    type_title = GOODS_TYPE[goods_list[0].goods_type_id]
    context = {
        'goods_list':goods_list,
        'goods_new_list':goods_new_list,
        'goods_type_id':goods_type_id,
        'type_title': type_title,
        'sort':sort,
        'pages':pages
    }

    return render(request,'df_goods/list.html',context)







# /goods/stock/数字/  获取商品的库存
def goods_stock(request):
    gid = request.GET.get('gid')
    res = 0
    return JsonResponse({'res':res})





