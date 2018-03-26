# -*- coding:utf-8 _*-  
__author__ = 'luyue'
""" 
@file: urls.py 
@time: 2018/03/{DAY} 
"""
from django.conf.urls import url, include

from .views import UserInfoView,UploadImageView, UploadPwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, MyFavView, MyMessageView

urlpatterns = [
    #用户个人信息展示 和  #用户个人中心修改资料
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    #用户头像上传
    url(r'^image_upload/$', UploadImageView.as_view(), name='image_upload'),
    #用户个人中心密码修改
    url(r'^update/pwd/$', UploadPwdView.as_view(), name='pwd_upload'),
    #用户邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    #用户个人中心修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='supdate_email'),
    #用户个人中心我的课程
    url(r'^my_course/$', MyCourseView.as_view(), name='my_course'),
    #用户个人中心我的收藏
    url(r'^my_fav/(?P<fav_type>\d+)/$', MyFavView.as_view(), name='my_fav'),
    #用户个人中心我的消息
    url(r'^my_message/$', MyMessageView.as_view(), name='my_message'),

]

