from django.shortcuts import render
from rateMyCourse.models import *
import json
# Create your views here.

from django.http import HttpResponse

def index(request):
    return render(request, "rateMyCourse/index.html")

def signIn1(request):
    textBox = request.GET.get('textBox');
    return HttpResponse("textBox: "+textBox)

#GET
def searchSchool(request):
    school = request.GET.get('school');
    keyword = request.GET.get('keyword');
    return HttpResponse("searchSchool school:"+school+" keyword:"+keyword)

#GET
def getIndex(request):
    return render(request, "rateMyCourse/index.html")

#GET
def getCourse(request, course_id):
    try:
        course = Course.objects.get(name=course_id)
    except Course.DoesNotExist:
        return HttpResponse("ERROR:No Such Course In Databases")
    result={
        'name': course.name,
        'department': course.department.name,
        'description': course.description
    }
 #   return HttpResponse("getCourse course_id:"+course_id)
    return HttpResponse(json.dumps(result))

#POST
def signIn(request):
    username = request.POST['username']
    password = request.POST['password']
    return HttpResponse("signIn username: "+username+" password:"+password)

#POST
def signUp(request):
    username = request.POST['username']
    password = request.POST['password']
    mail = request.POST['mail']
    return HttpResponse("signUp username: "+username+" password:"+password+" mail:"+mail)

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
