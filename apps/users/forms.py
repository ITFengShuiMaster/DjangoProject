# -*- coding:utf-8 _*-
__author__ = 'luyue'
""" 
@file: forms.py 
@time: 2018/03/{DAY} 
"""

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile

import re

class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=20)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class ImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birday', 'gender', 'address', 'mobile']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        p = re.compile('1[345]\d{9}')
        if p.match(mobile):
            return mobile
        else:
            print('+++++++++++++++++++++++++++++++++++++++++')
            raise forms.ValidationError('手机号非法')
