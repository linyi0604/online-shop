
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.home_list_page ), #显示首页
    url(r'^goods/(?P<goods_id>\d+)/$',views.goods_detail ), # 显示商品的详细信息
    url(r'^stock/\d+/$' ,views.goods_stock ),  # 获取商品的库存量
    url(r'^list/(?P<goods_type_id>\d+)/(?P<pindex>\d+)/$' ,views.goods_list),  # /goods/list/种类/页码/？sort=排序方式  商品列表页



]
