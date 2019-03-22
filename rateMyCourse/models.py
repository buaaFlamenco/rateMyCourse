# -*- coding: UTF-8 -*-
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


class Teacher(models.Model):
    """
    Description of teachers. \n
    name: char, length = 64, the name of teacher \n
    website: URL, the (introduction) website of the teacher \n
    title: char, length = 64, the title of the teacher \n
    department: foreign key to table DEPARTMENT, defines which department that the teacher belongs to
    """
    name = models.CharField(max_length=64)
    website = models.URLField(blank=True)
    title = models.CharField(max_length=64)

    # connections
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.name


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
    role = models.CharField(max_length=1, choices=ROLE_CHOICE)
    self_introduction = models.CharField(max_length=256, blank=True, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)

    def __str__(self):
        return self.username


class Course(models.Model):
    """
    Table of users. \n
    username: char, length = 64, the name of the course \n
    website: URL, the (introduction) website of the course \n
    ID: char, length = 50, unique ID of the class, primary key \n
    description: char, length = 512, the description of the class, including time, place and so on \n
    average_rank: float, the average rank of the class \n
    course_type: tuple, the type of the course \n
    """
    # todo mo detailed course type
    COURSE_TYPE_CHOICE = (
        ('C', 'Compulsory '),
        ('S', 'Selective'),
        ('G', 'General'),
    )

    # attributes
    name = models.CharField(max_length=64)
    website = models.URLField()
    ID = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=512, blank=True)
    average_rank = models.FloatField()
    course_type = models.CharField(max_length=1, choices=COURSE_TYPE_CHOICE)

    def __str__(self):
        return self.name


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
    edit_time = models.DateTimeField


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
    create_time = models.DateTimeField()
    edit_time = models.DateTimeField()
    parent_comment = models.IntegerField(default=-1)

    def __str__(self):
        return self.id


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
