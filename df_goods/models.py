from django.db import models
from db.base_model import BaseModol
from db.base_manager import BaseManager
from .enums import *
from tinymce.models import HTMLField
# Create your models here.


class GoodsManager(BaseManager):
    '''商品模型管理器类'''
    def get_goods_by_type(self,goods_type_id,limit=None,order_by=('-pk', )):
        '''根据类型查询商品，可以限制 数量 和 排序方案,默认按照id降序'''
        # 按照查询条件和 排序条件 查询
        goods_list = self.get_ordered_object_list(filters={'goods_type_id':goods_type_id},order_by=order_by)
        # 如果限制取多少个 则切片
        if limit is not None:
            goods_list = goods_list[:limit]
        return goods_list

    def get_goods_by_id(self,goods_id):
        goods = self.get_one_object(id=goods_id)
        return goods





class Goods(BaseModol):
    '''商品模型类'''
    goods_type_choice = (
        (FRUIT,GOODS_TYPE[FRUIT]),
        (SEAFOOD,GOODS_TYPE[SEAFOOD]),
        (MEAT,GOODS_TYPE[MEAT]),
        (EGGS,GOODS_TYPE[EGGS]),
        (VEGETABLES,GOODS_TYPE[VEGETABLES]),
        (FROZEN,GOODS_TYPE[FROZEN])
    )
    goods_type_id=models.SmallIntegerField(choices=goods_type_choice,default=FRUIT,verbose_name='商品类型')
    goods_name = models.CharField(max_length=20,verbose_name='商品名称')
    goods_sub_title = models.CharField(max_length=128,verbose_name='商品副标题')
    goods_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品价格')
    transit_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品单位')
    goods_unite = models.CharField(max_length=10,verbose_name='商品单位')
    goods_info = HTMLField(verbose_name='商品描述') #使用富文本编辑器
    goods_image = models.ImageField(upload_to='goods',verbose_name='商品图片')
    goods_stock = models.IntegerField(default=0,verbose_name='商品库存')
    goods_sales = models.IntegerField(default=0,verbose_name='商品销量')

    goods_status_choice = (
        (OFFLINE,GOODS_STATUS[OFFLINE]),
        (ONLINE,GOODS_STATUS[ONLINE])
    )
    goods_status = models.SmallIntegerField(choices=goods_status_choice,default=ONLINE,verbose_name='商品状态')

    objects = GoodsManager()

    class Meta :
        db_table = 's_goods'




class ImageManager(BaseManager):
    '''商品详情信息管理类'''
    def get_image_by_goods_id(self,goods_id):
        images = self.get_ordered_object_list(filters={'goods_id':goods_id})
        print(images)
        if images.exists():
            images = images[0]
        return images


class Image(BaseModol):
    '''商品详情图片模型类'''
    goods = models.ForeignKey('Goods',verbose_name='所属商品')
    img_url = models.ImageField(upload_to='goods',verbose_name='详情图片')

    objects = ImageManager()

    class Meta:
        db_table='s_goods_image'

