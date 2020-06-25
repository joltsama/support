from django.contrib import admin
from django.urls import path
from . import views

app_name='predict'

urlpatterns = [
    path('', views.index, name='index'),
    path('gendata/', views.gen_random_data, name='newdata'),
    path('chart/', views.CurrentTimings, name='chart'),
    path('simulate/', views.simulate, name='simulate'),
    path('simulatedata/', views.simulatedata, name='simulatedata'),
    path('change/', views.change, name='change')
]
  