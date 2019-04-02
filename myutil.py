import json
import datetime
import logging
import obj_sqlalchemy
# import mysite
# class MyModel:
#     @classmethod
#     def create(c,data):
#         id=data.get("id")
#         logging.info(id)
#         if id==None or id=="":
#             obj=c()
#             fields=c._meta.fields
#             for f in fields:
#                 if f.name!="id":
#                     exec("obj.%s=data['%s']" % (f.name,f.name))
#             return obj
#         else:
#             obj=c.objects.get(id=int(id))
#             fields=c._meta.fields
#             for f in fields:
#                 logging.info(dir(f))
#                 if f.name!="id":
#                     exec("obj.%s=data['%s']" % (f.name,f.name))
#             return obj
#     def json(self):
#         fields=type(self)._meta.fields
#         dic1={}
#         for f in fields:
#             # if type(f)==models.FileField:
#             #     exec("dic1['%s']=self.%s" % (f.name,f.name))
#             # else:
#             exec("dic1['%s']=self.%s" % (f.name,f.name))
#         return dic1
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        #logging.info(obj)
        if isinstance(obj,datetime.date):
            return "%d-%02d-%02d" % (obj.year,obj.month,obj.day)
        if isinstance(obj,datetime.datetime):
            return "%d-%02d-%02d" % (obj.year,obj.month,obj.day)
        if isinstance(obj,obj_sqlalchemy.PartsItem):
            return obj.name
        if isinstance(obj,obj_sqlalchemy.PartsUsepack):
            return obj.id
        # if isinstance(obj,FieldFile):
        #     #logging.info(dir(obj))
        #     return obj.name
        if isinstance(obj,obj_sqlalchemy.PartsContact):
            return obj.hetongbh        
        return json.JSONEncoder.default(self, obj)