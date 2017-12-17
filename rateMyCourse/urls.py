from django.conf.urls import url, include
from django.contrib import admin
from .views import pages, api, register

urlpatterns = [
    #GET
    url(r'^$', pages.getIndex, name='getIndex'),
    url(r'^index/$', pages.getIndex, name='getIndex'),
    url(r'^search/$', pages.search, name='search'),
    url(r'^course/(?P<course_number>[0-9A-Z\-]+)/$', pages.coursePage, name='coursePage'),
    url(r'^course/(?P<course_number>[0-9A-Z\-]+)/rate/$', pages.ratePage, name='ratePage'),
    url(r'^user/(?P<username>.+)/$', pages.userPage, name='userPage'),
    # 普通访问这个url返回信息不包含匿名信息
    # 要包含匿名信息需要发POST请求，请求中包含password，这里面是md5加密后的密码。
    # 加密后的密码已经存到cookie中，直接$.cookie('password')就能拿到
    
    #POST
    url(r'^signIn/$', register.signIn, name='signIn'),
    url(r'^signUp/$', register.signUp, name='signUp'),
    url(r'^active/(?P<active_code>.*)/$', register.active, name="active"),
    url(r'^submitComment/$', api.submitComment, name='submitComment'),
    url(r'^submitDiscuss/$', api.submitDiscuss, name='submitDiscuss'),

    #TMP GET IN INDEX
    url(r'^getSchool/$', api.getSchool, name='getSchool'),
    url(r'^getDepartment/$', api.getDepartment, name='getDepartment'),
    url(r'^getCourse/$', api.getCourse, name='getCourse'),
    url(r'^getComment/$', api.getComment, name='getComment'),
    url(r'^getDiscuss/$', api.getDiscuss, name='getDiscuss'),
    url(r'^getTeachers/$', api.getTeachers, name='getTeachers'),
    url(r'^getOverAllRate/$', api.getOverAllRate, name='getOverAllRate'),






    url(r'^addComment/(?P<commentID>[0-9A-Z]+)/$', pages.addCommentPage, name='addCommentPage'),
    url(r'^changeComment/$', api.changeComment, name='changeComment'),

    # post格式： {
    # 'comment_id': ...
    # 'comment_add': 要增加的评价内容
    # 'password': 加密后的密码
    # }

    url(r'^delComment/$', api.delComment, name='delComment'),

    # post格式： {
    # 'comment_id': ...
    # 'password': ...
    # }

    url(r'^changeSupport/$', api.changeSupport, name='changeSupport'),

    # post格式： {
    # 'comment_id': ...
    # 'username': ...
    # 'password': ...
    # }

    url(r'^delDiscuss/$', api.delDiscuss, name='delDiscuss'),

]
