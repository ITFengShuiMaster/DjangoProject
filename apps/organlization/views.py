from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from django import forms

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict
from .forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course
# Create your views here.


# ONE_PAGE_NUM = 1
#
#
# class OrgView(View):
#     def get(self, request):
#         try:
#             current_page = int(request.GET.get('current_page', '1'))
#             all_page = int(request.GET.get('all_page', '1'))
#             page_type = request.GET.get('page_type', '')
#         except Exception as e:
#             current_page = 1
#             all_page = 1
#             page_type = ''
#
#         if page_type == 'next':
#             current_page = current_page + 1
#         if page_type == 'last':
#             current_page = current_page - 1
#
#         start = (current_page - 1) * ONE_PAGE_NUM
#         end = start + ONE_PAGE_NUM
#
#         all_orgs = CourseOrg.objects.all()[start:end]
#
#         if current_page == 1 and all_page == 1:
#             all = CourseOrg.objects.count()
#             all_page = all // ONE_PAGE_NUM
#             if_has = all % ONE_PAGE_NUM
#             if if_has:
#                 all_page += 1
#
#         all_cities = CityDict.objects.all()
#         # orgs_len = all_orgs.count()
#         return render(request, 'org-list.html', {
#             'all_orgs': all_orgs,
#             'all_cities': all_cities,
#             'current_page': current_page,
#             'all_page': all_page,
#             'range_page': range(1, all_page+1),
#         })


class OrgView(View):
    def get(self, request):
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger as e:
            page = 1

        hot_orgs = CourseOrg.objects.order_by('-click_nums')[:3]
        city_id = request.GET.get('city', '')
        ct = request.GET.get('ct', '')
        sort = request.GET.get('sort', '')

        all_orgs = CourseOrg.objects.all()
        all_cities = CityDict.objects.all()

        #城市筛选
        if city_id:
            all_orgs = all_orgs.filter(city_id=city_id)

        #机构类别筛选
        if ct:
            all_orgs = all_orgs.filter(catgory=ct)

        #机构排序
        if sort:
            all_orgs = all_orgs.order_by('-'+sort)

        org_nums = all_orgs.count()
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'people': orgs,
            'all_cities': all_cities,
            'city_id': city_id,
            'ct': ct,
            'org_nums': org_nums,
            'hot_orgs': hot_orgs,
            'sort': sort,
            'index_type': 'course_org'
        })


class AddUserAskView(View):
    def get(self, request):
        pass

    def post(self, request):
        try:
            user_ask_form = UserAskForm(request.POST)
            if user_ask_form.is_valid():
                user = user_ask_form.save(commit=True)
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg": "添加错误"}', content_type='application/json')
        except forms.ValidationError as e:
            print(e.code)
            print('++++++++----------------------')
            return HttpResponse("{'status': 'fail', 'msg': {0}}".format(e.code))


class OrgHomeView(View):
    '''
    机构首页
    '''

    def get(self,request,org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        teacher = course_org.teacher_set.all()[:1]
        has_fav = False
        if request.user.is_authenticated():
            user_fav = UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2)
            if user_fav:
                has_fav = True

        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'teachers': teacher,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    '''
    机构课程
    '''

    def get(self, request, org_id):
        current_page = 'courses'
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1

        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()

        p = Paginator(all_courses, 3, request=request)
        people = p.page(page)

        return render(request, 'org-detail-course.html', {
            'course_org': course_org,
            'people': people,
            'current_page': current_page,
        })


class OrgDescView(View):
        '''
        机构课程
        '''

        def get(self, request, org_id):
            current_page = 'desc'
            try:
                page = request.GET.get('page', 1)
            except:
                page = 1

            course_org = CourseOrg.objects.get(id=int(org_id))
            all_courses = course_org.course_set.all()

            p = Paginator(all_courses, 3, request=request)
            people = p.page(page)

            return render(request, 'org-detail-desc.html', {
                'all_courses': all_courses,
                'course_org': course_org,
                'people': people,
                'current_page': current_page,
            })


class OrgTeacherView(View):
    '''
    机构课程
    '''

    def get(self, request, org_id):
        current_page = 'teacher'
        try:
            page = request.GET.get('page', 1)
        except:
            page = 1

        course_org = CourseOrg.objects.get(id=int(org_id))
        teachers = course_org.teacher_set.all()

        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'current_page': current_page,
            'teachers': teachers,
        })


class AddFavView(View):
    def post(self, request):
        user = request.user
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        else:
            exist_user_fav = UserFavorite.objects.filter(user=user, fav_id=int(fav_id), fav_type=int(fav_type))
            if exist_user_fav:
                #如果存在记录，那么代表用户取消掉收藏
                exist_user_fav.delete()
                # return JsonResponse('{"status":"fail", "msg":"收藏"}')
                return HttpResponse('{"status":"fail", "msg":"收藏"}', content_type='application/json')
            else:
                #否则代表用户添加收藏
                user_fav = UserFavorite()
                if int(fav_id) > 0 and int(fav_type) > 0:
                    user_fav.user = request.user
                    user_fav.fav_id = int(fav_id)
                    user_fav.fav_type = int(fav_type)
                    user_fav.save()
                    # return JsonResponse('{"status":"fail", "msg":"已收藏"}')
                    return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')
