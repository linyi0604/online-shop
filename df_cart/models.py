from django.db import models
from db.base_manager import BaseManager
from db.base_model import BaseModol
from df_goods.models import Goods
from django.db.models import Sum
# Create your models here.

class CartAdmin(BaseManager):
    '''购物车模型管理器类'''
    def add_goods(self,goods_id,goods_count,passport_id):
        '''
        添加商品进购物车
            如果购物车已经有该商品就修改数量
            如果购物车中没有这个商品 就添加商品
        '''
        res = self.get_one_object(goods_id=goods_id,passport_id=passport_id)
        # 首先拿到这个商品的库存
        goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
        goods_stock = goods.goods_stock
        if res:  #如果购物车中已经有这个商品
            if goods_stock< res.goods_count + goods_count:  #库存不足 不能加入购物车
                return False
            # 正常加入购物车 修改该商品在购物车中的数量
            res.goods_count = goods_count + res.goods_count
            res.save()
            return True

        else :  #购物车没有这个商品
            if goods_count > goods_stock:   #如果库存不足 返回False
                return False
            #向数据库插入一条
            Cart.objects.add_one_object(goods_id=goods_id,goods_count=goods_count,passport_id=passport_id)
            return True

    def get_cart_count(self,passport_id):
        '''获取用户购物车商品总数量'''
        res = self.filter(passport_id = passport_id).aggregate(Sum('goods_count'))
        if res['goods_count__sum'] is None:
            return 0
        else :
            return res['goods_count__sum']

    def get_cart_by_passort(self,passport_id):
        '''通过用户id查询该用户的购物车内所有物品'''
        cart = self.filter(passport_id=passport_id)
        return cart

    def update_cart_info(self,passport_id, goods_id, goods_count):
        '''更新购物车记录信息'''
        cart_info = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        if goods_count<= cart_info.goods.goods_stock:
            #库存充足
            cart_info.goods_count = goods_count
            cart_info.save()
            return True
        else :
            #库存不足
            return False

    def get_cart_list_by_cart_id_list(self,cart_id_list):
        return self.get_ordered_object_list(filters={'id__in':cart_id_list })


    def del_goods(self,goods_id,passport_id):
        '''根据用户id和商品id删除购物车中某个商品的记录'''
        goods = self.get_one_object(goods_id=goods_id,passport_id=passport_id)
        if goods is None :
            return False
        else :
            goods.delete()
            return True
    def get_amount_annd_count_by_id_list(self,cart_id_list):
        '''计算商品的总数目和总价钱'''
        cart_list = self.get_ordered_object_list(filters={'id__in':cart_id_list })
        total_count,total_price = 0,0   # 保存商品数目和总价格
        for cart_info in cart_list: # 计算商品总数目和总价格
            total_count += cart_info.goods_count
            total_price += cart_info.goods_count*cart_info.goods.goods_price
        return total_count,total_price


class Cart(BaseModol):
    '''购物车模型类'''
    passport = models.ForeignKey('df_user.PassPort',verbose_name='账户')
    goods = models.ForeignKey('df_goods.Goods',verbose_name='商品')
    goods_count = models.IntegerField(verbose_name='商品数量')

    objects = CartAdmin()

    class Meta:
        db_table = 's_cart'



class BrowseHistoryAdmin(BaseManager):
    '''历史浏览记录模型管理器'''
    # 查询一条浏览信息
    def get_one_history(self,passport_id,goods_id):
        return self.get_one_object(passport_id=passport_id,goods_id=goods_id)

    # 更新历史浏览记录
    def add_one_history(self,passport_id,goods_id):
        '''如果有，更新时间，如果没有，增加一条'''
        his = self.get_one_history(passport_id=passport_id,goods_id=goods_id)
        if his is None:
            self.add_one_object(passport_id=passport_id,goods_id=goods_id)
        else:
            his.save() #更新updatetime

    # 获取用户历史浏览记录
    def get_history_by_passport(self,passport_id,limit=5):
        '''
        返回用户的最近浏览记录４条
        没有返回None
        不够4条全部返回
        '''
        his_li = self.get_ordered_object_list(filters={'passport_id':passport_id},order_by=('-update_time',))
        if len(his_li) == 0 or his_li== None:
            return None
        elif len(his_li) < 4:
            return his_li
        else:
            return his_li[:5]



class BrowseHistory(BaseModol):
    '''历史浏览记录模型类'''
    passport = models.ForeignKey('df_user.PassPort',verbose_name='用户')
    goods = models.ForeignKey('df_goods.Goods',verbose_name='商品')

    objects = BrowseHistoryAdmin()

    class Meta :
        db_table = 's_browse_history'