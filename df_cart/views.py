from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from utils.decorators import login_required
from .models import Cart
# Create your views here.


# /cart/add/
@require_GET
@login_required
def cart_add(request):
    '''购物车添加商品'''
    # 1 获取用户id 商品id 和商品数量
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')

    # 2 调用添加方法 返回是否成功
    res = Cart.objects.add_goods(goods_id = goods_id,goods_count = int(goods_count),passport_id=passport_id)
    if res is True:
        # 添加成功了
        return JsonResponse({'res':1})
    else:
        #添加失败了
        return JsonResponse({'res':0})


# /cart/count/      获取购物车商品总数量
@require_GET
def cart_count(request):
    # 获取该用户的id
    passport_id = request.session.get('passport_id')
    # 查询该用户数据库中所有商品数量
    res = Cart.objects.get_cart_count(passport_id=passport_id)
    return JsonResponse({"res":res})


# /cart/    显示购物车页面
@login_required
def cart_show(request):
    passport_id = request.session.get('passport_id')
    # 查询该用户的购物车内信息
    carts = Cart.objects.get_cart_by_passort(passport_id=passport_id)
    return render(request,'df_cart/cart.html',{'carts':carts})


# /cart/update/ 更新购物车数量
@login_required
@require_GET
def cart_update(request):
    # 1 接受参数
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')
    res = Cart.objects.update_cart_info(passport_id=passport_id,goods_id=goods_id,goods_count=int(goods_count) )
    if res is True: #更新成功
        return JsonResponse({'res': 1})
    else :  #库存不足 更新失败
        return JsonResponse({'res': 0})

@login_required
@require_GET
# /cart/del 删除购物中某个商品
def cart_del(request):
    # 获取商品goods_id 和用户passport_id
    goods_id = request.GET.get('goods_id')
    passport_id = request.session.get('passport_id')
    # 调用数据库方法 删除购物车中该商品的记录
    res = Cart.objects.del_goods(goods_id=goods_id,passport_id=passport_id)
    if res:
        return JsonResponse({'res':1})
    else :
        return JsonResponse({'res':0})
