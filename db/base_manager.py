from django.db import models
from copy import copy
class BaseManager(models.Manager):
    '''抽象模型管理器类'''
    def get_all_valid_fields(self):
        '''获取self所有有效属性列表'''
        attr_str_list = []  #用于存储所有属性名称
        attr_tuple = self.model._meta.get_fields() # 获取模型类的所有属性
        for attr in attr_tuple:
            if isinstance(attr,models.ForeignKey):
                attr_str_list.append( attr.name+'_id' )
            else:
                attr_str_list.append(attr.name)
        return attr_str_list


    def get_one_object(self,**kwargs):
        '''查询一个对象的方法'''
        try:
            obj = self.get(**kwargs)
        except self.model.DoesNotExist:
            obj = None
        return obj

    def add_one_object(self,**kwargs):
        '''增加一个对象的方法'''
        # 拿到模型类的所有属性
        fields = self.get_all_valid_fields()
        # 如果传来参数有不是模型类属性的，就删除
        kw = copy(kwargs)
        for key in kw :
            if key not in fields:
                kwargs.pop(key)
        obj = self.model(**kwargs)
        obj.save()
        return obj

    def get_ordered_object_list(self,filters={},order_by=('-pk',)):
        '''获取所有对象列表'''
        #按照给出条件查询并按照条件排序
        object_list = self.filter(**filters).order_by(*order_by)
        return object_list



