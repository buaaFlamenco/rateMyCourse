from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    #GET
    url(r'^$', views.getIndex, name='getIndex'),
    url(r'^index/$', views.getIndex, name='getIndex'),
    url(r'^search/$', views.search, name='search'),
    url(r'^course/(?P<course_number>[0-9A-Z\-]+)/$', views.coursePage, name='coursePage'),
    url(r'^course/(?P<course_number>[0-9A-Z\-]+)/rate/$', views.ratePage, name='ratePage'),

    #POST
    url(r'^signIn/$', views.signIn, name='signIn'),
    url(r'^signUp/$', views.signUp, name='signUp'),
    url(r'^submitComment/$', views.submitComment, name='submitComment'),
    url(r'^submitDiscuss/$', views.submitDiscuss, name='submitDiscuss'),

    #TMP GET IN INDEX
    url(r'^getSchool/$', views.getSchool, name='getSchool'),
    url(r'^getDepartment/$', views.getDepartment, name='getDepartment'),
    url(r'^getCourse/$', views.getCourse, name='getCourse'),
    url(r'^getComment/$', views.getComment, name='getComment'),
    url(r'^getDiscuss/$', views.getDiscuss, name='getDiscuss'),
    url(r'^getTeachers/$', views.getTeachers, name='getTeachers'),
    url(r'^getOverAllRate/$', views.getOverAllRate, name='getOverAllRate'),

    url(r'^user/(?P<username>.+)/$', views.userPage, name='userPage'),

    # 普通访问这个url返回信息不包含匿名信息
    # 要包含匿名信息需要发POST请求，请求中包含password，这里面是md5加密后的密码。
    # 加密后的密码已经存到cookie中，直接$.cookie('password')就能拿到


    url(r'^addComment/(?P<commentID>[0-9A-Z]+)/$', views.addCommentPage, name='addCommentPage'),
    url(r'^changeComment/$', views.changeComment, name='changeComment'),

    # post格式： {
    # 'comment_id': ...
    # 'comment_add': 要增加的评价内容
    # 'password': 加密后的密码
    # }

    url(r'^delComment/$', views.delComment, name='delComment'),

    # post格式： {
    # 'comment_id': ...
    # 'password': ...
    # }

    url(r'^changeSupport/$', views.changeSupport, name='changeSupport'),

    # post格式： {
    # 'comment_id': ...
    # 'username': ...
    # 'password': ...
    # }

    url(r'^delDiscuss/$', views.delDiscuss, name='delDiscuss'),

]
