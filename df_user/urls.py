
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$',views.login),    #登录页面
    url(r'^logout/$',views.logout),    #退出登录 重定向到首页
    url(r'^login_check',views.login_check), #登录功能的实现
    url(r'^register/$',views.register),  #显示注册页面 和 注册功能
    url(r'^check_user_exist/$',views.check_user_exist),  #检查用户名是否重复
    url(r'^$',views.user ), #跳转到用户中心个人信息页面
    url(r'^address/$',views.address),   #用户中心地址页面
    url(r'^order/(\d*)/?$' , views.order ),    #用户中心 个人订单页面



]
