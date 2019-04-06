import json
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from random import Random  # 用于生成随机码

from django.conf import settings
from django.http import HttpResponse

from rateMyCourse.models import *

def make_comment(request):
    """
    发表评论，需要用户名，课程ID，以及内容
    """
    try:
        username = request.POST['username']
        course_ID = request.POST['course_ID']
        content = request.POST['content']
    except:
        return HttpResponse(json.dumps({
            'status': -1,
            'errMsg': '缺失信息',
        }))
    else:
        try:
            c = Comment(content=content)
            c.save()
            b = MakeComment(user=User.objects.get(username=username),
                          course=Course.objects.get(course_ID=course_ID),
                          comment=c)
            b.save()
        except:
            return HttpResponse(json.dumps({
                'status': -1,
                'errMsg': '发表评论失败',
            }))
        else:
            return HttpResponse(json.dumps({
                'status': 1,
                'length': 1,
                'body': {
                    'message': "发表评论成功"
                }
            }))

def get_comment_by_course(request):
    """
    获取某节课的评论，需求课程号
    返回一个列表，每项为一条评论，时间顺序
    """
    try:
        course_ID = request.GET['course_ID']
        rawList = MakeComment.objects.filter(course_id=Course.objects.get(course_ID=course_ID).id)

        retList = []
        for i in rawList:
            rdict = {}
            rdict['username'] = i.user.username
            rdict['content'] = i.comment.content
            rdict['editTime'] = str(i.comment.edit_time)
            rdict['createTime'] = str(i.comment.create_time)
            rdict['commentID'] = i.id
            retList.append(rdict)

    except:
        return HttpResponse(json.dumps({
            'status': -1,
            'errMsg': '获取评论失败',
        }))
    else:
        return HttpResponse(json.dumps({
            'status': 1,
            'length': len(rawList),
            'body': retList
        }))
    finally:
        pass

def edit_comment(request):
    """
    编辑评论，需求评论ID,新的content
    """
    try:
        c = MakeComment.objects.get(id=request.POST['ID'])
        c.comment.content = request.POST['content']
        c.comment.edit_time = datetime.datetime.now()
        c.comment.save()
    except:
        return HttpResponse(json.dumps({
            'status': -1,
            'errMsg': '更新评论失败',
        }))
    else:
        return HttpResponse(json.dumps({
            'status': 1,
            'length': 1,
            'body': {'message': "新建授课信息成功"}
        }))


