# #! /usr/bin/env python
# # -*- coding: utf-8 -*-
# # __author__ = "DaChao"
# # Date: 2017/9/20
#
# class playAppRouter(object):  # 配置app02的路由，去连接hvdb数据库
#     """
#     A router to control all database operations on models in the app02 application.
#     """
#
#     def db_for_read(self, model, **hints):
#         """
#         Attempts to read app02 models go to hvdb DB.
#         """
#         if model._meta.app_label == 'playApp':  # app name（如果该app不存在，则无法同步成功）
#             return 'db1'  # hvdb为settings中配置的database节点名称，并非db name。dbname为testdjango
#         return None
#
#     def db_for_write(self, model, **hints):
#         """
#         Attempts to write app02 models go to hvdb DB.
#         """
#         if model._meta.app_label == 'playApp':
#             return 'db1'
#         return None
#
#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Allow relations if a model in the app02 app is involved.
#         当 obj1 和 obj2 之间允许有关系时返回 True ，不允许时返回 False ，或者没有 意见时返回 None 。
#         """
#         if obj1._meta.app_label == 'playApp' or \
#                         obj2._meta.app_label == 'playApp':
#             return True
#         return None
#
#     def allow_migrate(self, db, model):
#         """
#         Make sure the app02 app only appears in the hvdb database.
#         """
#         if db == 'db1':
#             return model._meta.app_label == 'playApp'
#         elif model._meta.app_label == 'playApp':
#             return False
#
#     def allow_syncdb(self, db, model):  # 决定 model 是否可以和 db 为别名的数据库同步
#         if db == 'db1' or model._meta.app_label == "playApp":
#             return False  # we're not using syncdb on our hvdb database
#         else:  # but all other models/databases are fine
#             return True
#         return None
