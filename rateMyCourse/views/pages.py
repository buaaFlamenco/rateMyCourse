from rateMyCourse.models import *
from django.shortcuts import render, get_list_or_404, get_object_or_404
import json
from urllib import request, parse
from django.http import HttpResponse
from django.utils import timezone
import hashlib

detail_names = ['有趣程度', '充实程度', '课程难度', '课程收获']


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

def addHitCount():
	try:
		hit = HitCount.objects.get(name='hit')
	except Exception:
		hit = HitCount(name='hit', count=0)
		hit.save()
	hit.count += 1
	hit.save()



def getIndex(request):
    addHitCount()
    return render(request, "rateMyCourse/index.html")



def solrSearch(keywords, school, department):
    url = "http://10.2.28.123:8080/solr/collection1/select?q=%s&rows=100&wt=json&indent=true"
    keys = dict()

    ######
    # this is a fool idea to fix bug that if nothing to write in nothing you can search
    if(school == None and keywords == '\"\"'):
    	school = "北京航空航天大学"
    ######

    if(school != None):
        keys['school_name'] = school
    if(department != None):
        keys['department_name'] = department
    if(len(keywords) != 0):
        keys['course_name'] = keywords
    s = ' '.join([
        '+' + key + ':' + keys[key] + '' for key in keys
    ])
    t = request.urlopen(url%parse.quote(s)).read().decode('utf-8')
    t = json.loads(t)
    return [i['course_number'] for i in t['response']['docs']]

def search(request):
    addHitCount()
    keywords = request.GET['keywords']
    if('school' in request.GET):
        school = request.GET['school']
    else:
        school = None
    if('department' in request.GET):
        department = request.GET['department']
    else:
        department = None
    courselist = solrSearch(keywords, school, department)
    courses = []
    pages = []
    for i, c_number in enumerate(courselist):
        if(c_number in courselist[:i]):
            continue
        cs = Course.objects.filter(number=c_number)
        if(len(cs) == 0):
            continue
        x = getAvgScore(cs)
        courses.append({
            'name': cs[0].name,
            'ID': cs[0].number,
            'type': cs[0].coursetype,
            'credit': cs[0].credit,
            'school': cs[0].department.school.name,
            'department': cs[0].department.name,
            'rateScore': sum(x) / len(x),
            'ratenumber': sum([i.comment_set.count() for i in cs])
            })

    pn=int(len(courses)/10)+1
    for i in range(pn):
        pages.append({'number': i+1})
    return render(request, "rateMyCourse/searchResult.html", {
    	'courses': courses,
    	'count': len(courses),
    	'pages': pages,
    	})


def coursePage(request, course_number):
	addHitCount()
	courses = get_list_or_404(Course, number=course_number)
	x = getAvgScore(courses)
	return render(request, "rateMyCourse/coursePage.html", {
		'course_name': courses[0].name,
		'course_credit': courses[0].credit,
		'course_profession': courses[0].department.name,
		'course_type': courses[0].department.name,
		'course_scores': '%.1f'%(sum(x) / 4),
		'detail_names': detail_names,
		'detail_scores': x,
		'course_website': courses[0].website if courses[0].website != '' else '.',
        'profession_website': couses[0].department.website if courses[0].department.website != '' else '.',
		})




def ratePage(request, course_number):
    addHitCount()
    cs = get_list_or_404(Course, number=course_number)
    return render(request, "rateMyCourse/ratePage.html", {
            'course': {
                'name': cs[0].name,
                'school': cs[0].department.school.name,
                'department': cs[0].department.name,
            },
            'detail_names': detail_names,
        })


def userPage(request, username):
	user = get_object_or_404(User, username=username)
	try:
		pwd = request.POST['password']
	except:
		pwd = ""
	md5 = hashlib.md5()
	md5.update(user.password.encode('utf-8'))
	if(pwd == md5.hexdigest()):
		cmtList = user.comment_set.all()
	else:
		cmtList = user.comment_set.filter(anonymous=False)
	return render(request, "rateMyCourse/userPage.html", {
		'userName': username,
		'userimgurl': "../../static/ratemycourse/images/user.png", 
		'assessments': reversed(sorted([
			{
				'courseName': cmt.course.name,
				'course_id': cmt.course.number,
				'content': cmt.content,
				'time': cmt.time.strftime('%y/%m/%d'),
				'likeCount': cmt.support_set.count(),
				'commentCount': cmt.discuss_set.count(),
			}
			for cmt in cmtList
		], key=lambda t: t['time'])),
		'discussions': sorted(
        [
			{
				'userName': dsc.user.username,
				'userimgurl': "../../static/ratemycourse/images/user.png", 
				'course_id': dsc.comment.course.number,
				'content': dsc.content,
				'time': dsc.time.strftime('%y/%m/%d'),
				'title': dsc.comment.course.name,
				'originalContent': dsc.comment.content,
				'newmsg': dsc.newmsg,
			}
			for cmt in cmtList
				for dsc in cmt.discuss_set.all()
		] 
        + 
        [
            {
                'userName': dsc.user.username,
                'userimgurl': "../../static/ratemycourse/images/user.png", 
                'course_id': dsc.comment.course.number,
                'content': dsc.content,
                'time': dsc.time.strftime('%y/%m/%d'),
                'title': dsc.comment.course.name,
                'originalContent': dsc.comment.content,
                'newmsg': dsc.newmsg,
            }
            for dsc in user.aiteuser.all()
        ], key=lambda t: not t['newmsg'])
	})

def addCommentPage(request, commentID):
    print(commentID)
    comment = get_object_or_404(Comment, id=int(commentID))
    return render(request, "rateMyCourse/addRatePage.html", {
        'course': {
            'name': comment.course.name,
            'school': comment.course.department.school.name,
            'department': comment.course.department.name,
            'term': comment.term,
            'teacher': comment.course.teacher_set,
            },
        'originalRate': comment.content,
        })