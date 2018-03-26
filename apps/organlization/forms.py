# -*- coding:utf-8 _*-  
__author__ = 'luyue'
""" 
@file: forms.py 
@time: 2018/03/{DAY} 
"""

from django import forms

from operation.models import UserAsk

import re


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        '''
        手机号码非法的验证
        :return:
        '''
        mobile = self.cleaned_data['mobile']
        RUST_LIKE = '1[345]\d{9}'
        p = re.compile(RUST_LIKE)
        if p.match(mobile):
            return mobile
        else:
            print('********************************************')
            raise forms.ValidationError('手机号非法', code='mobile_invalid')