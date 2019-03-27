import json
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from random import Random  # 用于生成随机码

from django.conf import settings
from django.http import HttpResponse

from rateMyCourse.models import *


def sign_up(request):
    """
    注册用户。传入POST，应至少包含 username, password, mail 三个键 \n
    对于正常合法传入，新建用户并返回成功信息（status=1） \n
    其他非法情况返回错误信息（status=-1） 错误信息保存在errMsg中 \n
    """
    try:
        username = request.POST['username']
        mail = request.POST['mail']
        password = request.POST['password']
    except Exception:
        return HttpResponse(json.dumps({
            'status': -1,
            'errMsg': '未能获取到用户名，邮箱或密码',
        }))
    try:
        User(username=username, mail=mail, password=password).save()
    except Exception as err:
        errmsg = str(err)
        if "mail" in errmsg:
            return HttpResponse(json.dumps({
                'status': -1,
                'errMsg': '此邮箱已经被注册过',
            }))
        elif "username" in errmsg:
            return HttpResponse(json.dumps({
                'status': -1,
                'errMsg': '此用户名已经被注册过',
            }))
        else:
            return HttpResponse(json.dumps({
                'status': -1,
                'errMsg': '邮箱或用户名已经被注册过',
            }))
    else:
        return HttpResponse(json.dumps({
            'status': 1,
            'length': 1,
            'body': {
                'message': "新建用户{0}成功".format(username)
            }
        }))


def update_user(request):
    """
    注册用户。传入POST，应至少包含 username, 其他可选项是role, gender, self introduction。 \n
    对于正常合法传入，更新用户信息并返回成功信息（status=1） \n
    其他非法情况返回错误信息（status=-1） 错误信息保存在errMsg中 \n
    """
    try:
        username = request.POST['username']
        user = User.objects.get(username=username)
    except Exception:
        return HttpResponse(json.dumps({
            'status': -1,
            'errMsg': '不存在此用户',
        }))
    else:
        try:
            user.gender=request.POST['gender']
            user.role=request.POST['role']
            user.self_introduction=request.POST['self_introduction']
            user.save()
        except Exception:
            return HttpResponse(json.dumps({
                'status': -1,
                'errMsg': '保存失败，请检查内容正确性',
            }))
        else:
            return HttpResponse(json.dumps({
                'status': 1,
                'length': 1,
                'body': {
                    'message': "用户{0}信息更新成功".format(username)
                }
            }))


def randomStr(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def sendRegisterEmail(user, receiver):
    #

    print(settings.HOST)
    emailRecord = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    code = randomStr(16)
    emailRecord.code = code
    emailRecord.name = user
    emailRecord.save()

    subject = "公客网站激活"
    body = "激活链接： " + settings.HOST + "active/" + code + "/"

    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = 'flamenco<' + settings.EMAIL_HOST_USER + '>'
    msg['To'] = receiver

    smtp = smtplib.SMTP()
    smtp.connect(settings.EMAIL_HOST)
    smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    a = smtp.sendmail(settings.EMAIL_HOST_USER, receiver, msg.as_string())
    smtp.quit()

    return HttpResponse(emailRecord)




def signIn(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': '未能获取到用户名，邮箱或密码',
        }))
    try:
        u = User.objects.get(username=username)
    except Exception:
        try:
            u = User.objects.get(mail=username)
        except Exception:
            return HttpResponse(json.dumps({
                'statCode': -2,
                'errormessage': '用户名或邮箱不存在',
            }))
    if (password != u.password):
        return HttpResponse(json.dumps({
            'statCode': -3,
            'errormessage': '密码错误',
        }))
    else:
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': username,
        }))
