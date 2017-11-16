'''自定义过滤器'''
from django.template import Library

# 创建一个Library类的对象
register = Library()


# 定义过滤器函数
@register.filter
def order_status(value):
    '''根据value 返回订单状态'''
    print(value,'jahahha')

    status_dict = {
        1:'未支付',
        2:'待发货',
        3:'待收货',
        4:'待评价',
        5:'已完成'
    }
    return status_dict[value]