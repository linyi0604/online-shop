from django.db import models
from db.base_model import BaseModol
from db.base_manager import BaseManager
# Create your models here.


class OrderBasicAdmin(BaseManager):
    '''订单基本信息管理类'''
    def add_one_basic_info(self,order_id,passport_id,addr_id,total_count,total_price,transit_price,pay_method):
        '''添加订单基本信息记录'''
        order_basic = self.add_one_object(order_id=order_id,passport_id=passport_id,addr_id=addr_id,total_count=total_count,total_price=total_price,transit_price=transit_price,pay_method=pay_method)
        return order_basic

    def get_order_basic_info_by_passport(self,passport_id):
        '''获取用户的订单信息'''
        order_basic_list = self.get_ordered_object_list(filters={'passport_id':passport_id})
        for order_basic in order_basic_list:
            order_basic.order_detail_list = OrderDetailInfo.objects.get_one_detail_info_by_order_id(order_id=order_basic.order_id)

        return order_basic_list

class OrderBasic(BaseModol):
    '''订单基本模型类'''
    order_id = models.CharField(primary_key=True,max_length=64,verbose_name='订单编号')
    passport = models.ForeignKey('df_user.PassPort',verbose_name='所属用户') # 外键
    addr = models.ForeignKey('df_user.Address',verbose_name='收货地址')
    total_count = models.IntegerField(default=1,verbose_name='商品总数')
    total_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品总价')
    transit_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='运费')
        # 支付方式 1货到付款 2威信支付 3支付宝 4银联
    pay_method = models.IntegerField(default=1,verbose_name='支付方式')
        # 订单状态 1 待支付 2待收货 3待评价 4已完成
    order_status = models.IntegerField(default=1,verbose_name='订单状态')

    objects = OrderBasicAdmin()

    class Meta:
        db_table = 's_order_basic'





class OrderDetailInfoAdmin(BaseManager):
    '''订单详情模型类'''
    def add_one_detail_info(self,order_id,goods_id,goods_count,goods_price):
        '''添加一条订单详情记录'''
        detail_info = self.add_one_object(order_id=order_id,goods_id=goods_id,goods_count=goods_count,goods_price=goods_price)
        return detail_info
    def get_one_detail_info_by_order_id(self,order_id):
        '''根据order_id查询订单详情'''
        order_detail_list = self.get_ordered_object_list(filters={"order_id":order_id})
        return order_detail_list

class OrderDetailInfo(BaseModol):
    '''订单详细模型类'''
    order = models.ForeignKey('OrderBasic',verbose_name='所属订单')
    goods = models.ForeignKey('df_goods.Goods',verbose_name='商品')
    goods_count = models.IntegerField(default=0,verbose_name='商品数目')
    goods_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品价格')

    objects = OrderDetailInfoAdmin()

    class Meta:
        db_table = 's_order_detail'

