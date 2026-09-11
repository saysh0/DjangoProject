from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from . import views

# urlpatterns = [path('hello/', views.hello, name='hello'),
#                path('create_task/', views.create_task, name='create_task'),
#                path('get_tasks/', views.get_tasks, name='get_tasks'),
#                path('get_task/<int:pk>/', views.get_task, name='get_task'),
#                path('tasks_stats/', views.task_stats, name='tasks_stats'),
#                path('subtasks/', views.SubTaskListCreateView.as_view(), name='subtasks-list-create'),
#                path('subtasks/<int:pk>/', views.SubTaskDetailUpdateDeleteView.as_view(), name='subtasks-detail'),]

# urlpatterns = [path('tasks/', views.TaskListCreateAPIView.as_view(), name='tasks_create_lsit'),
#                path('tasks/<int:pk>/', views.TaskRetrieveUpdateDestroyAPIView.as_view(), name='task_delete_update_details'),
#                path('subtask/', views.SubTaskListCreateAPIView.as_view(), name='subtask_create_lsit'),
#                path('subtask/<int:pk>/', views.SubTaskRetrieveUpdateDestroyAPIView.as_view(), name='subtask_delete_update_details'),
#                ]

router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'task', views.TaskViewSet)
router.register(r'subtask', views.SubTaskViewSet)

urlpatterns = [path('', include(router.urls)),
               path('token/', TokenObtainPairView.as_view(), name='token-obtain-payload'),
               path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
               path('register/', views.RegisterView.as_view(), name='register'),
               path('login/', views.LoginView.as_view(), name='login'),
               path('logout/', views.LogoutView.as_view(), name='logout'),
              ]