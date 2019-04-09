import hashlib
import json
from urllib import request, parse

from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404

from rateMyCourse.models import *

detail_names = ['有趣程度', '充实程度', '课程难度', '课程收获']


def searchTeacher(request):
    """
    搜索教师.
    教师姓名，空为任意教师
    姓名包含关键字的所有教师
    """
    retlist = []
    try:
        name = request.GET['name']
        teacher_list = Teacher.objects.filter(name__icontains=name)
        for teacher in teacher_list:
            retlist.append(teacher.ret())
    except Exception:
        return HttpResponse(json.dumps({
            'status': -1,
            'errMsg': 'teacher name Error',
        }), content_type="application/json")
<<<<<<< HEAD

=======
>>>>>>> d123996... Merge branch 'backend_refactoring' of https://github.com/supplient/rateMyCourse into backend_refactoring
    return HttpResponse(json.dumps({
        'status': 1,
        'length': len(teacher_list),
        'body': retlist,
    }), content_type="application/json")


def searchCourse(request):
    """
    搜索课程.
    课程姓名，空为任意课程
    姓名包含关键字的所有课程
    """
    retlist = []
    try:
        courseName = request.GET['Course']
        course_list = Course.objects.filter(name__icontains=courseName)
        for course in course_list:
            retlist.append(course.ret())
    except Exception:
        return HttpResponse(json.dumps({
            'status': -1,
            'errMsg': 'course name Error',
        }), content_type="application/json")
    return HttpResponse(json.dumps({
        'status': 1,
        'length': len(course_list),
        'body': retlist,
    }), content_type="application/json")
<<<<<<< HEAD
=======

>>>>>>> d123996... Merge branch 'backend_refactoring' of https://github.com/supplient/rateMyCourse into backend_refactoring

def searchUser(request):
    """
    搜索用户.
    用户姓名，空为任意用户
    姓名包含关键字的所有用户
    """
    retlist = []
    try:
        username = request.GET['username']
        user_list = User.objects.filter(name__icontains=username)
        for user in user_list:
            retlist.append(user.ret())
    except Exception:
        return HttpResponse(json.dumps({
            'status': -1,
            'errMsg': 'user name Error',
        }), content_type="application/json")
    return HttpResponse(json.dumps({
        'status': 1,
        'length': len(user_list),
        'body': retlist,
    }), content_type="application/json")
