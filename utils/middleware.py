
class UrlPathRecordMiddleware(object):
    '''记录访问url地址记录中间件类'''
    # 不记录的列表
    exclude_path = ['/user/login/','/user/register/','/user/logout/']
    def process_view(self,request,view_func,*view_args,**view_kwargs):
        # 发来的请求不是ajax并且 不在上面列表中，我们记录仪下他上次访问的地方
        #当用于访问哪里跳到登录后 再跳转回来
        if request.path not in UrlPathRecordMiddleware.exclude_path and not request.is_ajax():
            request.session['pre_url_path'] = request.path



