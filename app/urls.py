from django.urls import path
from . import views

urlpatterns = [path('hello/', views.hello, name='hello'),
               path('create_task/', views.create_task, name='create_task'),
               path('get_tasks/', views.get_tasks, name='get_tasks'),
               path('get_task/<int:pk>/', views.get_task, name='get_task'),
               path('tasks_stats/', views.task_stats, name='tasks_stats')]