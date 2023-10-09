from django.contrib import admin
from django.urls import path,include, re_path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('', views.home, name='homepage'),
    re_path('newproject', views.createNewProject, name=''),
    re_path('proj', views.createNewProject, name=''),
    re_path('notes', views.AddNotes),
    re_path('pending', views.showPending),
    re_path('complete', views.markComplete),
    re_path('submitted', views.showCompleted),
    re_path("delete", views.delete)
]
