from django.shortcuts import render, get_list_or_404, get_object_or_404
from rateMyCourse.models import *
import json
from urllib import request, parse
from django.http import HttpResponse
from django.utils import timezone
import hashlib

from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from django.conf import settings
# Create your views here.

def addHitCount():
    try:
        hit = HitCount.objects.get(name='hit')
    except Exception:
        hit = HitCount(name='hit', count=0)
        hit.save()
    hit.count += 1
    hit.save()

def getAvgScore(courses):
    x = [0] * 4
    count = 0
    for c in courses:
        for rate in c.rate_set.all():
            x[0] += rate.A_score
            x[1] += rate.B_score
            x[2] += rate.C_score
            x[3] += rate.D_score
            count += 1
    if(count > 0):
        for i in range(4):
            x[i] /= count
    return x




def getSchool(request):
    result = {
        'school': [s.name for s in School.objects.all()],
    }
    return HttpResponse(json.dumps(result))

def getDepartment(request):
    try:
        school = School.objects.get(name=request.GET['school'])
    except Exception as err:
        return HttpResponse(json.dumps({
            'error': 'school not found'
            }))
    return HttpResponse(json.dumps({
        'department': [d.name for d in school.department_set.all()]
        }))

def getCourse(request):
    try:
        school = School.objects.get(name=request.GET['school'])
        department = school.department_set.get(name=request.GET['department'])
    except Exception as err:
        return HttpResponse(json.dumps({
            'error': 'school or department not found'
            }))
    return HttpResponse(json.dumps({
        'course': [c.name for c in department.course_set.all()]
        }))

def getComment(request):
    try:
        username = request.GET['username']
    except Exception:
        username = None

    try:
        courses = Course.objects.filter(number=request.GET['course_number'])
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get course_number or course_number not exists',
            }))
    cmtList = []
    for c in courses:
        for cmt in c.comment_set.all():
            snum = 0
            support = 0
            cnum = 0
            sup = Support.objects.filter(comment=cmt)
            for s in sup:
                snum = snum+1
                if(s.user.username == username):
                    support = 1
            dis = Discuss.objects.filter(comment=cmt)
            for d in dis:
                cnum = cnum+1

            cmtList.append({
                'userName': cmt.user.username if cmt.anonymous == False else '匿名用户',
                'text': cmt.content.replace("\n", "<br/>"),
                'time': cmt.time.strftime('%y/%m/%d'),
                'iTerm': cmt.term,
                'iTeacher': ','.join([t.name for t in cmt.course.teacher_set.all()]),
                'iTotal': cmt.total_score,
                'iId': cmt.id,
                'isSelf': 1 if(cmt.user.username == username) else 0,
                'snum': snum,# 点赞总数
                'cnum': cnum,#讨论总数
                'support': support,#是否支持
                })
    return HttpResponse(json.dumps({
        'statCode': 0,
        'comments': cmtList,
        }))

def getDiscuss(request):
    try:
        discusses = Discuss.objects.filter(comment_id=request.GET['iId'])
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get comment_id or comment_id not exists',
            }))
    disList = []
    for discuss in discusses:
        disList.append({
            'userName': discuss.user.username,
            'text': discuss.content.replace("\n", "<br/>"),
            'time': discuss.time.strftime('%y/%m/%d'),
            'discuss_id': discuss.id,
            })
    return HttpResponse(json.dumps({
        'statCode': 0,
        'discusses': disList,
        }))

def getTeachers(request):
    try:
        courses = Course.objects.filter(number=request.GET['course_number'])
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get course_number or course_number not exists',
            }))
    tList = []
    for c in courses:
        tList.append([
            t.name for t in c.teacher_set.all()
            ])
    return HttpResponse(json.dumps({
        'statCode': 0,
        'teachers': tList,
        }))

def getOverAllRate(request):
    try:
        courses = Course.objects.filter(number=request.GET['course_number'])
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get course_number or course_number not exists',
            }))
    return HttpResponse(json.dumps({
        'statCode': 0,
        'rate': getAvgScore(courses),
        }))


def submitComment(request):
    addHitCount()
    try:
        username = request.POST['username']
        comment = request.POST['comment']
        rate = request.POST.getlist('rate')
        for i, j in enumerate(rate):
            rate[i] = int(j)
        course_number = request.POST['course_number']
        anonymous = request.POST['anonymous']
        term = request.POST['term']
        teacher = request.POST.getlist('teacher')
    except Exception as err:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'post information not complete! ',
            }))
    cset = Course.objects.filter(number=course_number)
    # print(rate, teacher)
    for t in teacher:
        cset = cset.filter(teacher_set__name=t)
    # print(cset)
    # assert(len(cset) == 1)
    crs = cset[0]

    if(Comment.objects.filter(
        course=crs, user=User.objects.get(username=username)
        ).count() >= 2):
        return HttpResponse(json.dumps({
            'statCode': -2,
            'errormessage': 'you have made 3 comments ont this course',
            }))


    # print(anonymous)
    Comment(
        anonymous=True if anonymous == 'true' else False,
        content=comment,
        time=timezone.now(),
        user=User.objects.get(username=username),
        course=crs,
        term=term,
        total_score = sum(rate) / len(rate),
        ).save()
    Rate(
        user=User.objects.get(username=username),
        course=crs,
        A_score=rate[0],
        B_score=rate[1],
        C_score=rate[2],
        D_score=rate[3],
        ).save()
    return HttpResponse(json.dumps({
        'statCode': 0,
        }))

def submitDiscuss(request):
    addHitCount()
    try:
        username = request.POST['username']
        discuss = request.POST['discuss']
        comment_id = request.POST['comment_id']
        newmsg = 1
    except Exception as err:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'post information not complete! ',
            }))
    Discuss(
        content=discuss,
        time=timezone.now(),
        user=User.objects.get(username=username),
        newmsg=newmsg,
        comment=Comment.objects.get(id=comment_id),
        ).save()
    return HttpResponse(json.dumps({
        'statCode': 0,
        }))

def changeComment(request):
    try:
        commentID = request.POST['comment_id']
        commentAdd = request.POST['comment_add']
        password = request.POST['password']
    except Exception as err:
        print(err)
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'post information not complete! ',
            }))

    try:
        comment = Comment.objects.get(id=commentID) 
    except Exception as err:
        return HttpResponse(json.dumps({
            'statCode': -2,
            'errormessage': 'this id is not matched with any comment',
            }))

    md5 = hashlib.md5()
    md5.update(comment.user.password.encode('utf-8'))
    if(password != md5.hexdigest()):
        return HttpResponse(json.dumps({
            'statCode': -3,
            'errormessage': 'password validate failed',
            }))

    comment.content += '\n\n'+commentAdd
    comment.save()
    return HttpResponse(json.dumps({
        'statCode': 0,
        }))

def delComment(request):
    try:
        commentID = request.POST['comment_id']
        password = request.POST['password']
    except Exception as err:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'post information not complete! ',
            }))
    try:
        comment = Comment.objects.get(id=commentID) 
    except Exception as err:
        return HttpResponse(json.dumps({
            'statCode': -2,
            'errormessage': 'this id is not matched with any comment',
            }))

    md5 = hashlib.md5()
    md5.update(comment.user.password.encode('utf-8'))
    if(md5.hexdigest() != password):
        return HttpResponse(json.dumps({
            'statCode': -2,
            'errormessage': 'password validate failed',
            }))

    comment.delete()
    return HttpResponse(json.dumps({
        'statCode': 0,
        }))

def changeSupport(request):
    print(request.POST)
    try:
        commentID = request.POST['comment_id']
        username = request.POST['username']
        password = request.POST['password']
    except Exception as err:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'post information not complete! ',
            }))
    try:
        comment = Comment.objects.get(id=commentID) 
        user = User.objects.get(username=username)
    except Exception as err:
        return HttpResponse(json.dumps({
            'statCode': -2,
            'errormessage': 'this commentID or username is not matched with any ',
            }))

    md5 = hashlib.md5()
    md5.update(user.password.encode('utf-8'))
    if(md5.hexdigest() != password):
        return HttpResponse(json.dumps({
            'statCode': -3,
            'errormessage': 'password validate failed',
            }))

    try:
        support=Support.objects.get(comment=comment,user=user)
    except Exception as supportFlag:
        Support(
            comment=comment,
            user=user,
            ).save()
        return HttpResponse(json.dumps({
            'statCode': 0,
            }))

    support.delete()
    return HttpResponse(json.dumps({
        'statCode': 1,
        }))


def delDiscuss(request):
    try:
        discussID = request.POST['discuss_id']
        password = request.POST['password']
    except:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'post information not complete! ',
            }))

    try:
        discuss = Discuss.objects.get(id=DiscussID)
    except:
        return HttpResponse(json.dumps({
            'statCode': -2,
            'errormessage': 'this id is bot matched with any discuss',
            }))

    md5 = hashlib.md5()
    md5.update(discuss.user.password)
    if(md5.hexdigest() != password):
        return HttpResponse(json.dumps({
            'statCode': -3,
            'errormessage': 'password validate failed',
            }))

    discuss.delete()

    return HttpResponse(json.dumps({
        'statCode': 0,
        }))