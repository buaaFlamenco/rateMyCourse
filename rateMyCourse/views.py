from django.shortcuts import render, get_object_or_404
from rateMyCourse.models import *
import json
from django.http import HttpResponse,Http404
# Create your views here.

from django.http import HttpResponse


#GET
def getIndex(request):
    return render(request, "rateMyCourse/index.html")


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
def search(request):
    keywords = request.GET['keywords']
    if('school' in request.GET):
        school = request.GET['school']
    else:
        school = None
    if('department' in request.GET):
        department = request.GET['department']
    else:
        department = None
    ## here for searching algrithm

    ### this is for test
    courselist = Course.objects.all()[0:100]
    ###
    courses = []
    n_list = set()
    for c in courselist:
        if c.number in n_list:
            continue
        n_list.add(c.number)
        try:
            overallrate = c.rate_set.get(overallrate=True)
        except Exception:
            Rate(overallrate=True, course=c, A_score=0, B_score=0, C_score=0, user=User.objects.get(username='overallrate')).save()
            overallrate = c.rate_set.get(overallrate=True)
        courses.append({
            'name': c.name,
            'ID': c.number,
            'type': c.coursetype,
            'credit': c.credit,
            'school': c.department.school.name,
            'department': c.department.name,
            'rateScore': sum([overallrate.A_score, overallrate.B_score, overallrate.C_score]) / 3,
            'ratenumber': sum([i.rate_set.count() - 1 for i in Course.objects.filter(number=c.number)])
            })
    return render(request, "rateMyCourse/searchResult.html", {'courses': courses})
    
#GET
def coursePage(request, course_number):
    get_object_or_404(Course, number=course_number)
    courses = Course.objects.filter(number=course_number)
    return render(request, "rateMyCourse/coursePage.html", {
            'course_number': courses[0].number,
            'course_name': courses[0].name,
            'course_description': courses[0].description if courses[0].description != '' else 'we have no description',
            'course_website': courses[0].website if courses[0].website != '' else 'we have no website',
            'course_credit': courses[0].credit,
            'course_teachers': [(t.name for t in c.teacher_set.all()) for c in courses],
            'aspect1': '课程难度',
            'aspect2': '课程质量',
            'aspect3': '考核方式',
        })

def ratePage(request, course_number):
    c = get_object_or_404(Course, number=course_number)
    return render(request, "rateMyCourse/ratePage.html", {
            'course_name': c.name,
            'course_school': c.department.school.name,
            'course_department': c.department.name,
            'aspect1': '课程难度',
            'aspect2': '课程质量',
            'aspect3': '考核方式',
        })

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

def getComment(request):
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
            cmtList.append({
                'username': cmt.user.username,
                'content': cmt.content,
                'time': cmt.time.__str__(),
                'teachers': [t.name for t in cmt.course.teacher_set.all()],
                })
    return HttpResponse(json.dumps({
        'statCode': 0,
        'comments': cmtList,
        }))

def getOverAllRate(request):
    try:
        courses = Course.objects.filter(number=request.GET['course_number'])
    except Exception:
        return HttpResponse(json.dumps({
            'statCode': -1,
            'errormessage': 'can not get course_number or course_number not exists',
            }))
    r = [0] * 3
    count = 0
    for c in courses:
        try:
            overallrateEntry = c.rate_set.get(overallrate=True)
        except Exception:
            Rate(overallrate=True, course=c, A_score=0, B_score=0, C_score=0, user=User.objects.get(username='overallrate')).save()
            overallrateEntry = c.rate_set.get(overallrate=True)
        cnt = c.rate_set.count() - 1
        r[0] += overallrateEntry.A_score * cnt
        r[1] += overallrateEntry.B_score * cnt
        r[2] += overallrateEntry.C_score * cnt
        count += cnt
    if(count > 0):
        for i in range(len(r)):
            r[i] /= count
    return HttpResponse(json.dumps({
        'statCode': 0,
        'rate': r,
        }))
