from django.db import models
from db.base_model import BaseModol    #导入抽象模型基类
from db.base_manager import BaseManager
from utils.get_hash import get_hash

class PassPortAdmin(BaseManager):
    '''注册模型管理类'''
    def add_one_passport(self,username,password,email):
        '''添加一个注册用户到数据库'''
        obj = self.add_one_object(username=username,
                                  password=get_hash(password),
                                  email=email)
        return obj

    def check_user_exist(self,username):
        '''检查该用户名是否已经注册过'''
        obj = self.get_one_object(username=username)
        if obj is None:
            return False
        else :
            return True

    def getPassPort(self,username):
        '''通过用户名查询对象'''
        obj = self.get_one_object(username=username)
        return obj



class PassPort(BaseModol):
    '''账户模型'''
    username = models.CharField(max_length=20 ,verbose_name='账户名称')
    password = models.CharField(max_length=40,verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')

    objects = PassPortAdmin()

    class Meta:#指定数据库表名称
        db_table='s_user_account'





class AddressAdmin(BaseManager):
    '''地址模型管理类'''
    def get_default_address(self,passport_id):
        '''获取默认收货地址'''
        obj = self.get_one_object(passport_id=passport_id,is_default=True )
        return obj

    def add_one_addr(self,passport_id,recipient_name,recipient_addr,zip_code,recipient_phone):
        addr = self.get_default_address(passport_id)
        if addr is None:
            is_default = True
        else:
            is_default = False
        # 利用抽象管理器基类 添加一条数据
        obj = self.add_one_object(passport_id=passport_id,
                            recipient_name=recipient_name,
                            recipient_addr=recipient_addr,
                            zip_code=zip_code,
                            recipient_phone=recipient_phone ,
                            is_default=is_default )
        return obj



class Address(BaseModol):
    '''地址模型类'''
    passport = models.ForeignKey('PassPort',verbose_name='所属账户') #所属账户
    recipient_name = models.CharField(max_length=24,verbose_name='收件人')
    recipient_addr = models.CharField(max_length=256,verbose_name='收件地址')
    recipient_phone = models.CharField(max_length=11,verbose_name='联系电话')
    zip_code = models.CharField(max_length=6,verbose_name='邮政编码')
    is_default = models.BooleanField(default=False,verbose_name='是否默认') #是否默认地址

    objects = AddressAdmin()

    class Meta:
        db_table = 's_user_address'


















