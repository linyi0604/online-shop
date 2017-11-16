from django.shortcuts import render
from django.http import JsonResponse
from df_cart.models import Cart
from df_user.models import Address
from utils.decorators import login_required
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from datetime import datetime
from df_order.models import OrderBasic,OrderDetailInfo
from django.db import transaction   # 数据库的事物 实现原子性的操作
# Create your views here.


@login_required
@require_POST
# /order/   返回订单页面
def order_show(request):
    '''返回订单页面'''
    cart_id_list = request.POST.getlist('cart_id_list')
    passport_id = request.session.get('passport_id')
    cart_list = Cart.objects.get_cart_list_by_cart_id_list(cart_id_list=cart_id_list)
    addr = Address.objects.get_default_address(passport_id=passport_id)
    # 把cart_id_list 转换成字符串 传到前台
    cart_id_list = ','.join(cart_id_list)
    context = {
        'cart_list': cart_list,
        'addr': addr,
        'cart_id_list':cart_id_list
    }
    return render(request,'df_order/place_order.html',context)


@require_POST
@login_required
# /order/commit/    提交生成订单
@transaction.atomic  # 装饰这个函数 这个函数变成了数据库事物，如果执行失败会回滚
def order_commit(request):
    '''生成订单'''
    # 获取参数
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_style')
    cart_id_list = request.POST.get('cart_id_list')
    passport_id = request.session.get('passport_id')
    # 组织订单基本信息数据
    # orderid： 年月日十分秒 加上passport_id
    order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(passport_id)
    transit_price = 10
    # 获取商品的总数和总价格
    cart_id_list = cart_id_list.split(',')
    total_count , total_price = Cart.objects.get_amount_annd_count_by_id_list(cart_id_list=cart_id_list)

    # 设置一个保存点 如果后面问题 可以回复当前这个状态 对数据库数据没有改变
    sid = transaction.savepoint()
    try:
        # 添加订单基本信息记录
        OrderBasic.objects.add_one_basic_info(order_id=order_id,passport_id=passport_id,addr_id=addr_id,total_count=total_count,total_price=total_price,transit_price=transit_price,pay_method=pay_method)
        # 添加订单详细信息记录
        cart_list = Cart.objects.get_cart_list_by_cart_id_list(cart_id_list=cart_id_list)
        for cart_info in cart_list:
            # 组织订单详细记录数据
            goods_id = cart_info.goods_id
            goods_count = cart_info.goods_count
            goods_price = cart_info.goods.goods_price
            # 商品库存充足
            if cart_info.goods.goods_stock >= goods_count:
                # 添加订单详细记录
                OrderDetailInfo.objects.add_one_detail_info(order_id=order_id,goods_id=goods_id,goods_count=goods_count,goods_price=goods_price)
                # 更新商品的库存和销量
                cart_info.goods_count-=cart_info.goods_count
                cart_info.goods.goods_sales += cart_info.goods_count
                cart_info.goods.save()
                # 删除购物车中对应记录
                cart_info.delete()
            else:   #商品库存不充足
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res':0})

    except :
        # 发生异常说明订单生成发生错误 进行回滚
        transaction.savepoint_rollback(sid)
        return JsonResponse({'res':2})

    # 订单生成成功
    transaction.savepoint_commit(sid)
    return JsonResponse({'res':1})
