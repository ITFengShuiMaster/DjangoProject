# _*_ encoding:utf-8 _*_

from datetime import datetime

from django.db import models

from organlization.models import CourseOrg

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='课程名')
    description = models.CharField(max_length=300, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(max_length=2, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), verbose_name='难度')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name='封面图', max_length=100)
    category = models.CharField(default='', max_length=20, verbose_name='课程类别')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, blank=True)
    you_needed_konw = models.CharField(max_length=30, default='', verbose_name='课程须知')
    teacher_tell = models.CharField(max_length=50, default='', verbose_name='老师告诉你能学到什么')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def get_lesson_nums(self):
        return self.lesson_set.all().count()

    def __str__(self):
        return '{0}'.format(self.name)


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.course, self.name)


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视屏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.lesson, self.name)


class CourseResouce(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=100, verbose_name='名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name