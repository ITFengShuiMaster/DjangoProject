from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponse
from pure_pagination import Paginator, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, ImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.LoginViewMinmix import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from courses.models import Course, CourseOrg
from organlization.models import Teacher

import json
# Create your views here


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html', {})
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})

            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_forms': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            pass_word = request.POST.get('password', '')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'msg': '邮箱已注册', 'register_form': register_form})

            user_profile = UserProfile()
            user_profile.username = user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()

            print("发送前")
            send_register_email(user_name, 'register')
            return render(request, 'login.html', {})
        return render(request, 'register.html', {'register_form': register_form})


class ActiveView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        print(active_code)
        if all_record:
            for record in all_record:
                email = record.email
                try:
                    user = UserProfile.objects.get(email=email)
                    user.is_active = True
                    user.save()
                except Exception as e:
                    print('email 不存在')
        else:
            return render(request, 'active_error.html')
        return render(request, 'login.html')


class ForgetPasswdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email')
            if send_register_email(email=email, send_type='forget'):
                return render(request, 'send_success.html')
            else:
                print('邮件发送失败')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, reset_code):
        all_record = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_record:
            for record in all_record:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_error.html')


class ModifyView(View):
    def post(self, request):
        reset_form = ResetPwdForm(request.POST)
        if reset_form.is_valid():
            email = request.POST.get('email', '')
            pwd_1 = request.POST.get('password1', '')
            pwd_2 = request.POST.get('password2', '')
            if pwd_1 != pwd_2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd_1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'reset_form': reset_form})


class UserInfoView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        return render(request, 'usercenter-info.html', {
            'user_profile': user
        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)

        if user_info_form.is_valid():
            print('-------------------------------------')
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = ImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()


class UploadPwdView(View):
    def post(self, request):
        reset_form = ResetPwdForm(request.POST)
        if reset_form.is_valid():
            pwd_1 = request.POST.get('password1', '')
            pwd_2 = request.POST.get('password2', '')
            if pwd_1 != pwd_2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            request.user.password = make_password(pwd_1)
            request.user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(reset_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        if send_register_email(email, 'update_email'):
            return HttpResponse('{"status":"success"}', content_type='application/json')
        return HttpResponse('{"status":"failure"}', content_type='application/json')


class UpdateEmailView(View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')

        if not EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email'):
            return HttpResponse('{"email":"验证码错误"}', content_type='application/json')

        print('验证成功')
        request.user.email = email
        request.user.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')


class MyCourseView(View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses': user_courses
        })


class MyFavView(View):
    def get(self, request, fav_type):
        fav_type = int(fav_type)
        favs = UserFavorite.objects.filter(user=request.user, fav_type=fav_type)
        fav_things_id = [x.fav_id for x in favs]
        if fav_type == 1:
            courses = Course.objects.all().filter(id__in=fav_things_id)
            return render(request, 'usercenter-fav-course.html', {
                'courses': courses
            })
        elif fav_type == 2:
            orgs = CourseOrg.objects.all().filter(id__in=fav_things_id)
            return render(request, 'usercenter-fav-org.html', {
                'orgs': orgs
            })
        elif fav_type == 3:
            teachers = Teacher.objects.all().filter(id__in=fav_things_id)
            return render(request, 'usercenter-fav-teacher.html', {
                'teachers': teachers
            })


class MyMessageView(View):
    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger as e:
            page = 1

        p = Paginator(all_messages, 5, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {
            'all_messages': messages,
        })
