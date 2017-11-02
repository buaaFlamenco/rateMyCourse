from django.shortcuts import render, get_object_or_404
from rateMyCourse.models import *
import json
from django.http import HttpResponse,Http404
# Create your views here.

from django.http import HttpResponse


def signUp(request):
    try:
        username = request.POST['username']
        mail = request.POST['mail']
        password = request.POST['password']
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get username or mail or password',
            }))
    try:
        User(username=username, mail=mail, password=password).save()
    except Exception as err:
        errmsg = str(err)
        if("mail" in errmsg):
            return HttpResponse(json.dumps({
                'statCode': -2,
                'errormessage': 'mail repeated',
                }))
        elif("username" in errmsg):
            return HttpResponse(json.dumps({
                'statCode': -3,
                'errormessage': 'username repeated',
                }))
        else:
            return HttpResponse(json.dumps({
                'statCode': -4,
                'errormessage': 'other error, maybe out of length',
                }))
    else:
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': username,
            }))

    '''
    textBox = request.GET.get('textBox');
    return HttpResponse("textBox: "+textBox)
    '''

#GET
def searchSchool(request):
    school = request.GET.get('school');
    keyword = request.GET.get('keyword');
    return HttpResponse("searchSchool school:"+school+" keyword:"+keyword)

#GET
def getIndex(request):
    return render(request, "rateMyCourse/index.html")

#GET
def coursePage(request, course_number):
    course = get_object_or_404(Course, number=course_number)
    return render(request, "rateMyCourse/coursePage.html", {
            'course_number': course.number,
            'course_name': course.name,
            'course_description': course.description if course.description != '' else 'we have no description',
            'course_website': course.website if course.website != '' else 'we have no website',
            'course_credit': course.credit,
        })
    pass

#POST
def signIn(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get username or mail or password',
            }))
    try:
        u = User.objects.get(username=username)
    except Exception:
        try:
            u = User.objects.get(mail=username)
        except Exception:
            return HttpResponse(json.dumps({
            'statCode': -2,
            'errormessage': 'username or mail mot exists',
            }))
    if(password != u.password):
        return HttpResponse(json.dumps({
            'statCode': -3,
            'errormessage': 'wrong password',
            }))
    else:
        return HttpResponse(json.dumps({
            'statCode': 0,
            'username': username,
            }))

#POST
def courseAddComment(request):
    username = request.POST['username']
    content = request.POST['content']
    parentId = request.POST['parentId']
    courseId = request.POST['courseId']

    return HttpResponse("courseAddComment: "+username+content+parentId+content)

#POST
def courseAddRate(request):
    username = request.POST['username']
    rate = request.POST['rate']
    courseId = request.POST['courseId']
    return HttpResponse("courseAddRate: "+username+rate+courseId)

#GET TMP IN INDEX
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
