# _*_ coding:utf-8 _*_
__author__ = 'luyue'
__date__ = '2018/3/17 14:50'

import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'description', 'add_time']
    search_fields = ['name', 'description']
    list_filter = ['name', 'description', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'description', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'description', 'click_nums', 'fav_nums', 'image', 'address', 'city']
    list_filter = ['name', 'description', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']


class TeacherAdmin(object):
    list_display = [
        'course_org', 'name', 'work_years', 'work_company', 'work_position',
        'points', 'click_nums', 'fav_nums', 'add_time'
                    ]
    search_fields = [
        'course_org', 'name', 'work_years', 'work_company', 'work_position',
        'points', 'click_nums', 'fav_nums'
                    ]
    list_filter = [
        'course_org', 'name', 'work_years', 'work_company', 'work_position',
        'points', 'click_nums', 'fav_nums', 'add_time'
                    ]


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
