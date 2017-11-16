from django.shortcuts import redirect



#一个装饰器 如果用户登陆了 就正常做 否则就跳转到登录页面去
def login_required(view_func):
    '''登录判断装饰器'''
    def wrapper(request,*view_args,**view_kwargs):
        if request.session.has_key('islogin'):
            # 如果用户已经登录
            return view_func(request,*view_args,**view_kwargs)
        else:
            # 用户没有登录跳转到登录页面
            return redirect('/user/login/')


    return wrapper