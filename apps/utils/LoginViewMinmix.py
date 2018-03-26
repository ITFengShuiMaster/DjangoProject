# -*- coding:utf-8 _*-  
__author__ = 'luyue'
""" 
@file: LoginViewMinmix.py 
@time: 2018/03/{DAY} 
"""

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#判断用户是否登录,应该是权限问题
class LoginViewMix(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginViewMix, self).dispatch(request, *args, **kwargs)


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)