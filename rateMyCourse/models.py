# -*- coding: UTF-8 -*-
import datetime

from django.db import models


# Create your models here.

class Department(models.Model):
    """
    Description of departments. \n
    name: char, length = 64, the name of department \n
    website: URL, the (introduction) website of the department \n
    """
    name = models.CharField(max_length=64)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name

    def ret(self):
        return {
            'name': self.name,
            'website': self.website
        }


class Teacher(models.Model):
    """
    Description of teachers. \n
    name: char, length = 64, the name of teacher \n
    website: URL, the (introduction) website of the teacher \n
    title: char, length = 64, the title of the teacher \n
    //department: foreign key to table DEPARTMENT, defines which department that the teacher belongs to
    """
    name = models.CharField(max_length=64)
    website = models.URLField(blank=True)
    title = models.CharField(max_length=64, blank=True)

    '''# connections
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
    )'''

    def __str__(self):
        return self.name

    def ret(self):
        return {
            'name': self.name,
            'website': self.website,
            'title': self.title
        }


class User(models.Model):
    """
    Table of users. \n
    username: char, length = 64, the login name. must be unique \n
    mail: char, length = 64, the email address. must be unique \n
    password: char, length = 64, password, saved by md5+salt \n
    role: tuple, selected from T, S or O, representing the role of the user \n
    gender: tuple, selected from M, F or A, representing the gender of the user \n
    self_introduction: char, length = 256, the self introduction of the user, can be blank \n
    """
    ROLE_CHOICE = (
        ('T', 'Teacher'),
        ('S', 'Student'),
        ('O', 'Other'),
    )
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('A', 'Anonymous'),
    )

    # attributes
    username = models.CharField(max_length=64, unique=True)  # 用户名不可重复
    mail = models.EmailField(max_length=64, unique=True)
    # TODO md5+salt
    password = models.CharField(max_length=32)
    role = models.CharField(max_length=1, choices=ROLE_CHOICE, default='O')
    self_introduction = models.CharField(max_length=256, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default='A')

    def __str__(self):
        return self.username

    def ret(self):
        return {
            'username': self.username,
            'mail': self.mail,
            'role': self.role,
            'gender': self.gender,
            'self_introduction': self.self_introduction
        }


class Course(models.Model):
    """
    Table of users. \n
    name: char, length = 64, the name of the course \n
    website: URL, the (introduction) website of the course \n
    course_ID: char, length = 50, unique ID of the class, primary key \n
    description: char, length = 512, the description of the class, including time, place and so on \n
    # average_rank: float, the average rank of the class \n
    course_type: tuple, the type of the course \n
    credit: float, the credit of a course
    """
    '''# todo mo detailed course type
    COURSE_TYPE_CHOICE = (
        ('C', 'Compulsory '),
        ('S', 'Selective'),
        ('G', 'General'),
    )'''

    # attributes
    name = models.CharField(max_length=64)
    website = models.URLField()
    course_ID = models.CharField(max_length=50, unique=True, null=True)
    description = models.CharField(max_length=512, blank=True)
    # average_rank = models.FloatField()
    course_type = models.CharField(max_length=64, blank=True)
    credit = models.IntegerField()

    def __str__(self):
        return self.name

    def ret(self):
        return {
            'name': self.name,
            'website': self.website,
            'course_ID': self.course_ID,
            'description': self.description,
            'course_type': self.course_type,
            'credit': self.credit
        }


class TeachCourse(models.Model):
    """
    matches courses and their teachers together.\n
    teacher: ManyToManyField to table TEACHER, defines who teaches the course \n
    course: foreign key to table COURSE, defines the course \n
    department: foreign key to table DEPARTMENT, defines which department that this course belongs to \n
    """
    teachers = models.ManyToManyField(
        Teacher,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
    )


class Ranks(models.Model):
    """
    rank records. \n
    difficulty_score: difficulty of the course \n
    funny_score: how fun the course is \n
    gain_score: how much do you gain from the course \n
    recommend_score: the possibility of recommending the course to others \n
    edit_time: when the score is given\n
    """
    difficulty_score = models.FloatField(default=0)
    funny_score = models.FloatField(default=0)
    gain_score = models.FloatField(default=0)
    recommend_score = models.FloatField(default=0)
    edit_time = models.DateTimeField(default=datetime.datetime.now)

    def ret(self):
        return {
            'difficulty_score': self.difficulty_score,
            'funny_score': self.funny_score,
            'gain_score': self.gain_score,
            'recommend_score': self.recommend_score,
            'edit_time': self.edit_time
        }


class SelectCourse(models.Model):
    """
    match student with their courses. \n
    user: foreign key to table USER, defines who selects the course \n
    course: foreign key to table COURSE, defines which course that is selected \n
    ranks: foreign key to table RANKS, the detail of rank \n
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    ranks = models.ForeignKey(
        Ranks,
        on_delete=models.CASCADE,
    )


class Comment(models.Model):
    """
    details of each comment. \n
    content: char, length = 48. The main content of a comment \n
    create_time: DateTime, the time of create \n
    edit_time: Datetime, the time of last edit \n
    parent_comment: int, the id of it parent comment, default = -1 \n
    """
    content = models.CharField(max_length=2048)
    create_time = models.DateTimeField(default=datetime.datetime.now)
    edit_time = models.DateTimeField(default=datetime.datetime.now)
    parent_comment = models.IntegerField(default=-1)

    def __str__(self):
        return self.id

    def ret(self):
        return {
            'content': self.content,
            'create_time': self.create_time,
            'edit_time': self.edit_time,
            'parent_comment': self.parent_comment
        }


class MakeComment(models.Model):
    """
    match comments with the users that makes them. \n
    user: foreign key to table USER, defines whom the comment is created by \n
    course: foreign key to table COURSE, defines the course that this comment belongs \n
    comment: foreign key to table COMMENT, leads to the content of comment \n
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
    )


class HitCount(models.Model):
    name = models.CharField(max_length=50)
    count = models.IntegerField()

    def ret(self):
        return {
            'name': self.name,
            'count': self.count
        }
