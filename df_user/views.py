from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from . import tasks
from utils.decorators import *
from df_cart.models import BrowseHistory
from df_order.models import OrderBasic
from django.core.paginator import Paginator
# Create your views here.
'''
登录模块
'''
def login(request):
    '''返回登录页面'''
    username = request.COOKIES.get('username',"")
    return render(request,'df_user/login.html',{"username":username})


@require_POST
def login_check(request):
    '''登录功能的实现:
        *如果返回状态1  代表能够登录成功
        *如果返回状态2  代表登录用户名错误
        *如果返回状态3  代表密码错误
    '''
    username = request.POST.get('username')
    password = request.POST.get('password')
    secret_password = get_hash(password)
    passport = PassPort.objects.getPassPort(username)

    # 如果数据库里没有这个用户名
    if PassPort.objects.check_user_exist(username) == False:
        data = {'state':2}
        jre = JsonResponse(data)
    # 密码正确 能够成功登录
    elif passport.password == secret_password :
        #如果登录之前用户访问过某个页面，我们登录过后再跳回原来的页面
        if request.session.has_key('pre_url_path'):
            next = request.session.get('pre_url_path')
        else:
            next = '/index/'
        data = {
            'state':1,
            'username':username,
            'next':next,
        }
        jre = JsonResponse(data)
        # 如果点击了记住用户名，就设置cookie
        if request.POST.get('remember_user') == "true" :
            jre.set_cookie('username',username,max_age=7*24*60*60 )

        #记住用户登录的状态
        request.session['islogin'] = True
        request.session['username'] = username
        request.session['passport_id'] = passport.id

    # 如果密码不正确
    else :
        data = {'state': 3}
        jre = JsonResponse(data)

    return jre

# /user/logout  退出登录
def logout(request):
    '''用户退出登录'''
    request.session.flush() #删掉用户的登录信息
    return redirect('/')


'''
    用户注册模块
'''
# /user/register/   返回注册页面 、 完成注册功能
require_http_methods(['GET',"POST"])
def register(request):
    '''显示注册页面，用户注册功能'''
    if request.method == "GET" :
        return render(request,'df_user/register.html')
    else :
        '''实现用户信息的注册
            1 接收用户的注册信息
            2 保存到数据库
            3 跳转到登录页面
        '''
        # 1 接收用户注册信息
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        # 2 保存进数据库
        PassPort.objects.add_one_passport(username, password, email)
        # 3 发送邮件
        # 提交celery任务队列发送邮件
        # tasks.register_success_send_mail.delay(username, password, email)
        # 注册后直接发送邮件
        tasks.register_success_send_mail(username, password, email)
        return redirect('/user/login')


#/user/check_user_exist/   检查用户是否已经注册过
def check_user_exist(request):
    '''检查用户名是否重复'''
    username = request.POST.get('username')
    isRegistered = PassPort.objects.check_user_exist(username)
    return JsonResponse({'isRegistered':isRegistered})






'''
    用户中心部分
'''
# /user/  返回用户中心 个人信息页面
@login_required
def user(request):
    '''返回用户中心-个人信息页面'''
    passport_id = request.session.get("passport_id")
    #查询一下用户地址信息放入页面
    addr = Address.objects.get_default_address(passport_id=passport_id)
    # 查询一下用户历史浏览记录 放到页面
    his_li = BrowseHistory.objects.get_history_by_passport(passport_id=passport_id)
    context = {'page':'user','addr':addr,'his_li':his_li}
    return render(request , 'df_user/user_center_info.html',context)

# /user/address 用户信息的显示和编辑
@login_required
@require_http_methods(['GET','POST'])
def address(request):
    passport_id = request.session.get('passport_id')
    if request.method == 'GET':
        '''显示用户中心地址页面
            1 从数据库中查询默认收货地址
            2 将默认地址放入页面并返回 如果没有返回无
        '''
        default_addr = Address.objects.get_default_address(passport_id=passport_id)
        context = {
            'page':"addr",  #用于传递 当前点击了地址
            'addr':default_addr # 传递数据库查询结果 用户的默地址
            }
        return render(request,'df_user/user_center_site.html',context)
    else:
        '''
        添加收货地址：
            1 获取地址
            2 添加进数据库
            3 刷新页面 重定向
        '''
        recipient_name = request.POST.get('username')
        recipient_addr = request.POST.get('addr')
        recipient_phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')

        Address.objects.add_one_addr(passport_id=passport_id,
                                     recipient_name=recipient_name,
                                     recipient_addr=recipient_addr,
                                     zip_code=zip_code,
                                     recipient_phone=recipient_phone)


        return redirect('/user/address')


# /user/order/页码/
@login_required
def order(request,pindex):
    '''显示用户中心 个人订单'''
    passport_id = request.session.get('passport_id')
    # 查询用户的订单信息
    order_basic_list = OrderBasic.objects.get_order_basic_info_by_passport(passport_id=passport_id)


    # 对查询出来的商品进行分页操作
    paginator = Paginator(object_list=order_basic_list, per_page=1)
    if pindex == '':
        pindex = 1
    else:
        pindex = int(pindex)
    order_basic_list = paginator.page(pindex)  # 第pindex页数据
    nums = paginator.num_pages  # 分页之后的总页数
    # 调整分页列表 最多显示5页
    if nums <= 5:
        pages = range(1, nums + 1)
    elif pindex < 3:
        pages = range(1, 6)
    elif nums - pindex <= 2:
        pages = range(nums - 4, nums + 1)
    else:
        pages = range(pindex - 2, pindex + 3)

    context = {
        'page':"order",
        'order_basic_list':order_basic_list,
        'pages':pages
       }
    return render(request,'df_user/user_center_order.html',context)


