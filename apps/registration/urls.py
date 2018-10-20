from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^hacker$', views.hacker),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^message$', views.message),
    url(r'^comment$', views.comment),
    url(r'^delete$', views.delete)
]