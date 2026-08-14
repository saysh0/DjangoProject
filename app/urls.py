from django.urls import path
from . import views

# urlpatterns = [path('hello/', views.hello, name='hello'),
#                path('create_task/', views.create_task, name='create_task'),
#                path('get_tasks/', views.get_tasks, name='get_tasks'),
#                path('get_task/<int:pk>/', views.get_task, name='get_task'),
#                path('tasks_stats/', views.task_stats, name='tasks_stats'),
#                path('subtasks/', views.SubTaskListCreateView.as_view(), name='subtasks-list-create'),
#                path('subtasks/<int:pk>/', views.SubTaskDetailUpdateDeleteView.as_view(), name='subtasks-detail'),]

urlpatterns = [path('tasks/', views.TaskListCreateAPIView.as_view(), name='tasks_create_lsit'),
               path('tasks/<int:pk>/', views.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task_delete_update_details'),
               path('subtask/', views.SubTaskListCreateAPIView.as_view(), name='subtask_create_lsit'),
               path('subtask/<int:pk>/', views.SubTaskRetrieveUpdateDestroyAPIView.as_view(), name='subtask_delete_update_details'),
               ]