from celery import task
from django.conf import settings
from django.core.mail import send_mail



# 使用task装饰后 django就知道这个函数是一个任务 被调用就放进任务队列
# python manage.py celery worker --loglevel=info 打开服务器才能执行
@task
def register_success_send_mail(username,password,email):
    '''注册成功后给用户发送邮件'''
    msg = '<h1>欢迎注册天天生鲜会员！</h1> <br/>'\
          +' 请牢记你的个人信息: <br/>'+ '用户名:'+username+"<br/>密码："+password
    send_mail(subject='感谢注册',message="",from_email=settings.EMAIL_FROM,recipient_list=[email],html_message=msg)




