import os
import sys

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'flamenco.settings'
import django

django.setup()
from rateMyCourse.models import *
import pandas as pd

for m in [Teacher, Course, Department, TeachCourse, Ranks, SelectCourse, Comment, MakeComment]:
   m.objects.all().delete()

staticFilePath = "static/courseInfo/"
dfs = []
for file in os.listdir(staticFilePath):
    path = os.path.join(staticFilePath, file)
    dfs.append(pd.read_csv(open(path, encoding="utf-8")))

for i, df in enumerate(dfs):
    dfs[i] = df.drop_duplicates()
# department
department = set()

for df in dfs:
    for dep in df['开课学院'].unique():
        department.add(dep)
buf = []
for dep in department:
    buf.append(Department(name=dep, website="www.buaa.edu.cn"))
Department.objects.bulk_create(buf)
print("finish department")
# teacher
teacher = set()
for df in dfs:
    for entry in df.iterrows():
        entry = entry[1]
        tstr = entry['老师']
        for t in tstr.split('|'):
            if (len(t) == 3 and t[1] == ' '):
                t = t[0] + t[2]
            if (t == '暂无信息'):
                break
            if t not in teacher:
                teacher.add(t)
buf = []
for dep in teacher:
    buf.append(Teacher(name=dep, website="www.buaa.edu.cn", title="Teacher"))
Teacher.objects.bulk_create(buf)
print("finish teacher")
# course
course = dict()
for df in dfs:
    cnt=0
    for entry in df.iterrows():
        print(cnt)
        cnt += 1
        entry = entry[1]
        number = entry['课程编号']
        name = entry['课程名']
        course_type = entry['类型'] + ',' + entry['分类']
        credit = entry['学分']
        try:
            c = Course(course_type=course_type, name=name, course_ID=number, credit=credit, website="www.buaa.edu.cn")
            c.save()
        except:
            pass
        finally:
            pass
print("finish course")
# Teach Course
"""
matches courses and their teachers together.\n
teacher: ManyToManyField to table TEACHER, defines who teaches the course \n
course: foreign key to table COURSE, defines the course \n
department: foreign key to table DEPARTMENT, defines which department that this course belongs to \n
"""
for df in dfs:
    cnt=0
    for entry in df.iterrows():
        print(cnt)
        cnt+=1
        entry = entry[1]
        dep = Department.objects.get(name=entry['开课学院'])
        course = Course.objects.get(course_ID=entry['课程编号'])
        teacher = entry['老师'].split('|')
        for i, t in enumerate(teacher):
            if (len(t) == 3 and t[1] == ' '):
                teacher[i] = t[0] + t[2]
            if (t == '暂无信息'):
                teacher.remove(t)
        c = TeachCourse(course=course, department=dep)
        c.save()
        for i in teacher:
            c.teachers.add(Teacher.objects.get(name=i))
        c.save()
