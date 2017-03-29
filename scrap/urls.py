from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^fetchWeibo', views.fetchWeibo, name='fetchWeibo'),
    url(r'^scrapweibo', views.scrapweibo, name='scrapweibo'),
    url(r'^area', views.area, name='area'),
    url(r'^getcitiesinprovince', views.getCitiesInProvince, name='getcitiesinprovince'),
    url(r'^getareainCity', views.getAreaInCity, name='getareainCity'),
    url(r'^$', views.index, name='index')

               ]