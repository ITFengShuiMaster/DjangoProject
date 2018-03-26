# -*- coding:utf-8 _*-  
__author__ = 'luyue'
""" 
@file: urls.py 
@time: 2018/03/{DAY} 
"""
from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentsView, AddComments

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^details/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_details'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    url(r'^comments/(?P<course_id>\d+)/$', CourseCommentsView.as_view(), name='course_comments'),
    url(r'^add_comment/$', AddComments.as_view(), name='add_comments'),
]