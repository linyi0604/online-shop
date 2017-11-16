from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$', views.order_show), # 返回订单页面
    url('^commit/$',views.order_commit), #提交订单
]
