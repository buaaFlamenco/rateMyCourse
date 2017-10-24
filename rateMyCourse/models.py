from django.db import models


'''
网站功能
1. 课程信息
    1. Get & Set
        1. 课程名
        2. 课程内容简介
        3. 所属学校
        4. 所属专业
        5. 课程网站
2. 用户信息
    1. Get & Set
        1. 基本信息（学校、专业、年级）
        2. 评价列表
3. 总体评分
    1. Get & Set
        1. 所有评分表
        2. 各项评分
4. 具体评价
    1. Get & Set
        1. 评价日期
        2. 学期
        3. Tags
        4. 老师（和谐）
        5. 评价内容
        6. 各项评分
        7. 总共评分
        8. 评价下支持
        9. 评论下反对
        10. 评价下讨论
'''

# Create your models here.

class School(models.Model):
    # attributes
    name = models.CharField(max_length=50)

class Department(models.Model):
    # attributes
    name = models.CharField(max_length=50)
    website = models.URLField(null=True)

    # connections
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
    )

class Teacher(models.Model):
    # attributes
    name = models.CharField(max_length=50)
    website = models.URLField(null=True)
    
    # connections
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
    )

class User(models.Model):
    # attributes
    username = models.CharField(max_length=50, unique=True) # 用户名不可重复
    mail = models.EmailField(null=True)
    password = models.CharField(max_length=50)
    grade = models.CharField(max_length=50)
    reported = models.BooleanField()
    # connections
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
    )

class Course(models.Model):
    # attributes
    name = models.CharField(max_length=50)
    website = models.URLField(),
    description = models.CharField(max_length=2000)

    # connections
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
    )
    teachers = models.ManyToManyField(
        Teacher,
    )

class Comment(models.Model):
    # attributes
    conent = models.CharField(max_length=2000)
    time = models.DateTimeField()
    # connections
    fathercomment = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

class Rate(models.Model):
    # attributes
    overallrate = models.BooleanField()
    A_score = models.FloatField()
    B_score = models.FloatField()
    C_scroe = models.FloatField()
    # connections
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )