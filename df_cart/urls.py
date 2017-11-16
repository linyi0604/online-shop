from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^add/$', views.cart_add ),    #购物车添加商品
    url(r'^count/$',views.cart_count),  #获取购物车商品数量
    url(r'^$',views.cart_show),    # 显示购物车页面
    url(r'^update/$',views.cart_update), #更新购物车信息
    url(r'^del/$',views.cart_del)   # 删除购物车中的商品
]
