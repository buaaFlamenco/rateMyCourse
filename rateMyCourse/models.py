#-*- coding: UTF-8 -*-
from django.db import models
import datetime
# Create your models here.

class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    name = models.CharField(max_length=50, verbose_name=u"username")
    # 包含注册验证和找回验证
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.datetime.now)
    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)

class School(models.Model):
    # attributes
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Department(models.Model):
    # attributes
    name = models.CharField(max_length=50)
    website = models.URLField(blank=True)

    # connections
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
    )
    def __str__(self):
        return self.name

class Teacher(models.Model):
    # attributes
    name = models.CharField(max_length=50)
    website = models.URLField(blank=True)
    
    # connections
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
    )
    def __str__(self):
        return self.name

class User(models.Model):
    # attributes
    username = models.CharField(max_length=50, unique=True) # 用户名不可重复
    mail = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    # validationState = models.BooleanField(default=False)
    # validationCode = models.CharField(max_length=50)
    def __str__(self):
        return self.username

class Course(models.Model):
    # attributes
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    website = models.URLField()
    description = models.CharField(max_length=2000, blank=True)
    credit = models.FloatField()
    coursetype = models.CharField(max_length=50)

    # connections
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
    )
    teacher_set = models.ManyToManyField(
        Teacher,
    )
    def __str__(self):
        return self.name

class Comment(models.Model):
    # attributes
    anonymous = models.BooleanField(default=False)
    content = models.CharField(max_length=2000)
    time = models.DateTimeField()
    # connections
    # parentcomment = models.ForeignKey(
    #     'self',
    #     on_delete=models.SET_NULL,
    #     null=True,
    # )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    term = models.CharField(max_length=50)
    total_score = models.FloatField()
    
    def __str__(self):
        return self.content

class Rate(models.Model):
    # attributes
    A_score = models.FloatField(default=0) # 有趣程度
    B_score = models.FloatField(default=0) # 充实程度
    C_score = models.FloatField(default=0) # 课程难度
    D_score = models.FloatField(default=0) # 课程收货
    # connections
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return "rate from %s"%self.user

class Discuss(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
    )
    aiteuser = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="aiteuser",
        null=True,
    )
    time = models.DateTimeField()
    content = models.CharField(max_length=2000)
    newmsg = models.BooleanField(default=False)
        
class Support(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
    )
    newmsg = models.BooleanField(default=False)

class HitCount(models.Model):
    name = models.CharField(max_length=50)
    count = models.IntegerField()
