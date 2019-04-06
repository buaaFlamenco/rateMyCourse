from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(TeachCourse)
admin.site.register(Department)
admin.site.register(Teacher)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Course)
admin.site.register(Ranks)
admin.site.register(HitCount)
admin.site.register(SelectCourse)
admin.site.register(MakeComment)
