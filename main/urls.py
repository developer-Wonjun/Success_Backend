from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('main/start', views.start, name='start'),
    path('main/community/', views.home, name='home'),
    path('main/community/<int:blog_id>', views.detail, name='detail'),
    path('main/community/create/', views.create, name='create'),
    path('main/community/postcreate/', views.postcreate, name='postcreate'),
    path('main/community/new/', views.new, name='new'),
    path('main/update/<int:blog_id>', views.update, name='update'),
    path('delete/<int:blog_id>/', views.delete, name='delete'),
    path('main/alarm/', views.alarm, name='alarm'),
    path('main/map/', views.map, name='map'),
]
