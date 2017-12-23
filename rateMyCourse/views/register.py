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

def randomStr(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def sendRegisterEmail(user,receiver):
    #

    print(settings.HOST)
    emailRecord = EmailVerifyRecord()
    # 将给用户发的信息保存在数据库中
    code = randomStr(16)
    emailRecord.code = code
    emailRecord.name = user
    emailRecord.save()


    subject = "公客网站激活"
    body = "激活链接： "+settings.HOST+"active/"+code+"/"


    msg = MIMEText( body, 'plain', 'utf-8' )
    msg['Subject'] = Header( subject, 'utf-8' )
    msg['From'] = 'flamenco<'+settings.EMAIL_HOST_USER+'>'
    msg['To'] =  receiver

    smtp = smtplib.SMTP()
    smtp.connect(settings.EMAIL_HOST)
    smtp.login( settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD )
    a = smtp.sendmail( settings.EMAIL_HOST_USER, receiver, msg.as_string() )
    smtp.quit()

    return HttpResponse(emailRecord)


def active(request, active_code):
    try:
        all_recodes = EmailVerifyRecord.objects.filter(code=active_code)
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': '不存在该激活码',
        }))
    if all_recodes:
        for recode in all_recodes:
            username = recode.name
            try:
                user = User.objects.get(username=username)
            except Exception:
                return HttpResponse(json.dumps({
                    'statCode': -3,
                    'errormessage': '不存在此用户',
                    'username': username,
                }))
            if user.is_active:
                return HttpResponse(json.dumps({
                    'statCode': -4,
                    'errormessage': '此用户已被激活',
                    'username': username,
                }))

            user.is_active = True
            user.save()
            recode.delete()

    else:
        return HttpResponse(json.dumps({
            'statCode': -2,
            'errormessage': '不存在该激活码',
        }))

    return HttpResponse(user.username+'激活成功')



def signUp(request):
    try:
        username = request.POST['username']
        mail = request.POST['mail']
        password = request.POST['password']
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': '未能获取到用户名，邮箱或密码',
            }))
    try:
        User(username=username, mail=mail, password=password).save()
    except Exception as err:
        errmsg = str(err)
        if("mail" in errmsg):
            return HttpResponse(json.dumps({
                'statCode': -2,
                'errormessage': '该邮箱已被使用',
                }))
        elif("username" in errmsg):
            return HttpResponse(json.dumps({
                'statCode': -3,
                'errormessage': '该用户名已被使用',
                }))
        else:
            return HttpResponse(json.dumps({
                'statCode': -4,
                'errormessage': '输入字符过多',
                }))
    else:
        sendRegisterEmail(username, mail)
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': username,
            }))

    '''
    textBox = request.GET.get('textBox');
    return HttpResponse("textBox: "+textBox)
    '''


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
    if(password != u.password):
        return HttpResponse(json.dumps({
            'statCode': -3,
            'errormessage': '密码错误',
            }))
    else:
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': username,
            }))
