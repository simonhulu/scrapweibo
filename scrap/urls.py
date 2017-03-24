from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^fetchWeibo', views.fetchWeibo, name='fetchWeibo'),
    url(r'^$', views.index, name='index')

               ]