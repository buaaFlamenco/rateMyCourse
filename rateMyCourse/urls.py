from django.conf.urls import url, include
from django.contrib import admin
from .views import search,  register, models, comments

urlpatterns = [
    url(r'^signIn/$', register.sign_in, name='signIn'),
    url(r'^signUp/$', register.sign_up, name='signUp'),
    url(r'^updateUser/$', register.update_user, name='updateUser'),


    url(r'^searchTeacher/$', search.search_teacher, name='searchTeacher'),
    url(r'^searchCourse/$', search.search_course, name='searchCourse'),
    url(r'^searchUser/$', search.search_user, name='searchUser'),
    url(r'^searchCourseByDepartment/$', search.search_course_by_department,name='searchCourseByDepartment'),

    url(r'^addTeacher/$',models.add_teacher, name="addTeacher"),
    url(r'^addCourse/$',models.add_course, name="addCourse"),
    url(r'^addTeachCourse/$',models.add_teach_course, name="addTeachCourse"),

    url(r'^makeComment/$',comments.make_comment, name="makeComment"),
    url(r'^getCommentsByCourse/$',comments.get_comment_by_course, name="getCommentsByCourse"),
    url(r'^editComment/$',comments.edit_comment, name="editComments")

]
'''
urlpatterns = [
    #GET
    url(r'^$', search.getIndex, name='getIndex'),
    url(r'^index/$', search.getIndex, name='getIndex'),
    url(r'^search/$', search.search, name='search'),
    url(r'^course/(?P<course_number>[0-9A-Z\-]+)/$', search.coursePage, name='coursePage'),
    url(r'^course/(?P<course_number>[0-9A-Z\-]+)/rate/$', search.ratePage, name='ratePage'),
    url(r'^user/(?P<username>.+)/$', search.userPage, name='userPage'),
    # 普通访问这个url返回信息不包含匿名信息
    # 要包含匿名信息需要发POST请求，请求中包含password，这里面是md5加密后的密码。
    # 加密后的密码已经存到cookie中，直接$.cookie('password')就能拿到
    
    #POST
    url(r'^signIn/$', register.signIn, name='signIn'),
    url(r'^signUp/$', register.sign_up, name='signUp'),
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






    url(r'^addComment/(?P<commentID>[0-9A-Z]+)/$', search.addCommentPage, name='addCommentPage'),
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

'''
