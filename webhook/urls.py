from django.conf.urls import url, include
from .views import github

urlpatterns=[
    url(r'^github/$', github),
]