from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator,PageNotAnInteger


from .models import Course, CourseResouce
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.LoginViewMinmix import LoginViewMix,LoginRequiredMixin

# Create your views here.


class CourseListView(View):
    def get(self, request):
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger as e:
            page = 1

        sort = request.GET.get('sort', '')
        courses = Course.objects.all()

        keywords = request.GET.get('keywords', '')
        if keywords:
            courses = courses.filter(Q(name__icontains=keywords) | Q(description__icontains=keywords) | Q(detail__icontains=keywords))

        if sort:
            if sort == 'hot':
                courses = courses.order_by('-fav_nums')
            else:
                courses = courses.order_by('-students')
        else:
            courses = courses.order_by('-add_time')

        hot_courses = Course.objects.order_by('-fav_nums')[:3]
        p = Paginator(courses, 5, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'people': courses,
            'sort': sort,
            'hot_courses': hot_courses,
            'index_type': 'course',
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=int(course_id))
        except Exception as e:
            print('没有课程')

        #增加课程点击数
        course.click_num += 1
        course.save()
        has_course = False
        has_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type=1, fav_id=course_id):
                has_course = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=course.course_org.id):
                has_org = True
            return render(request, 'course-detail.html', {
                'course': course,
                'has_course': has_course,
                'has_org': has_org,
            })
        else:
            return render(request, 'course-detail.html', {
                'course': course,
            })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        try:
            exits_user_course = UserCourse.objects.filter(user=request.user, course_id=course_id)
            if not exits_user_course:
                user_course_add = UserCourse()
                user_course_add.user = request.user
                user_course_add.course_id = course_id
                user_course_add.save()

            course = Course.objects.get(id=course_id)
            course.students += 1
            course.save()
            user_course = UserCourse.objects.filter(course_id__in=course_id)
            user_ids = [user.user_id for user in user_course if user.user_id != request.user.id]
            user_course = UserCourse.objects.all().filter(user_id__in=user_ids)
            all_courses_ids = [x.course_id for x in user_course if x.course_id != course_id]
            print('***************************\n', all_courses_ids)
            all_courses = Course.objects.all().filter(id__in=all_courses_ids)
            print('***************************\n', all_courses)
        except:
            print('没有课程')
        return render(request, 'course-video.html', {
            'course': course,
            'all_courses': all_courses,
        })


class CourseCommentsView(View):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            comments = CourseComments.objects.filter(course=course)
            resource = CourseResouce.objects.filter(course_id=course_id)
        except Exception as e:
            print("没有该课程")
        return render(request, 'course-comment.html', {
            'course': course,
            'comments': comments,
            'resource': resource
        })


class AddComments(View):
    def post(self, request):
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')

        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')
        else:
            if int(course_id) > 0 and comments:
                add_comments = CourseComments()
                add_comments.comments = comments
                add_comments.user = request.user
                add_comments.course_id = course_id
                add_comments.save()
                return HttpResponse('{"status": "success", "msg": "添加成功"}', content_type='application/json')
            else:
                HttpResponse('{"status": "fail", "msg": "添加失败"}', content_type='application/json')
