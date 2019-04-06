import json
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from random import Random  # 用于生成随机码

from django.conf import settings
from django.http import HttpResponse

from rateMyCourse.models import *


def addTeacher(request):
    """
    增加教师，需求教师的基本信息：姓名，职称
    """
    try:
        name = request.POST['name']
        title = request.POST['title']
        try:
            website = request.POST['website']
        except:
            website = "null"
        Teacher(name=name,title=title,website=website).save()
    except Exception as err:
        if "unique" in str(err):
            return HttpResponse(json.dumps({
                'status': -1,
                'errMsg': 'teacher already exist',
            }), content_type="application/json")
        else:
            return HttpResponse(json.dumps({
                'status': -1,
                'errMsg': 'Operation Error',
            }), content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            'status': 1,
            'length': 1,
            'body': {
                'message': "新建教师{0}成功".format(name)
            }
        }), content_type="application/json")
    finally:
        pass


def addCourse(request):
    """
    增加课程，需求课程的基本信息：名字，网站，ID，描述，类型，学分
    """
    try:
        name = request.POST['name']
        website = request.Post['website']
        course_ID=request.POST['courseID']
        description = request.POST['description']
        course_type = request.POST['courseType']
        credit = request.POST['credit']
        Course(name=name,website=website,course_type=course_type,course_ID=course_ID,description=description,credit=credit).save()
    except Exception:
        return HttpResponse(json.dumps({
            'status': -1,
            'errMsg': 'Operation Error',
        }), content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            'status': 1,
            'length': 1,
            'body': {
                'message': "新建课程{0}成功".format(name)
            }
        }), content_type="application/json")
    finally:
        pass


def addTeachCourse(request):
    """
    增加课授课信息，需求教师列表，课程，部门
    """
    try:
        department=Department.objects.get(name=request.Post['department'])
        course=Course.objects.get(name=request.Post['course'])
        c=TeachCourse(department=department,course=course)
        c.save()
        for i in request.Post['teacherList']:
            c.teachers.add(Teacher.objects.get(name=i))
        c.save()
    except Exception:
        return HttpResponse(json.dumps({
            'status': -1,
            'errMsg': 'Operation Error',
        }), content_type="application/json")
    else:
        return HttpResponse(json.dumps({
            'status': 1,
            'length': 1,
            'body': {
                'message': "新建授课信息成功"
            }
        }), content_type="application/json")
    finally:
        pass

