from django.contrib.auth import authenticate
from django.db.models import Model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import TaskPermission, SubTaskPermission

from .models import *
from .permissions import SubTaskPermission
from.serializers import *
# Create your views here.

from django.http import HttpResponse

def hello(request):
    return HttpResponse('Hello, Nikita.')

# @api_view(['POST'])
# def create_task(request):
#     serializer = TaskSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# DAYS = {
#     'sunday': 1,
#     'monday': 2,
#     'tuesday': 3,
#     'wednesday': 4,
#     'thursday': 5,
#     'friday': 6,
#     'saturday': 7,
# }
#
# @api_view(['GET'])
# def get_tasks(request):
#     day_of_week = request.query_params.get('day_of_week')
#     if day_of_week:
#         number_day_of_week = DAYS.get(day_of_week)
#         tasks = Task.objects.filter(deadline__week_day=number_day_of_week)
#     else:
#         tasks = Task.objects.all()
#     serializer = TaskSerializer(tasks, many=True)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def get_task(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     serializer = TaskSerializer(task)
#     return Response(serializer.data)
#
# @api_view(['GET'])
# def task_stats(request):
#     tasks_count = Task.objects.all().count()
#     tasks_by_status_count = {}
#     for choice in Choices:
#         tasks_by_status_count[choice.value] = Task.objects.filter(status=choice).count()
#     overdue_tasks_count = Task.objects.filter(deadline__lt=timezone.now()).count()
#     return Response({'total': tasks_count, 'by_status': tasks_by_status_count, 'overdue': overdue_tasks_count})
#
# class SubTaskPaginator(PageNumberPagination):
#     page_size = 5
# class SubTaskListCreateView(APIView):
#     def get(self,request):
#         filter = {}
#         task = request.query_params.get('task')
#         subtask_status = request.query_params.get('subtask_status')
#         if task:
#             filter['task__title'] = task
#         if subtask_status:
#             filter['status__iexact'] = subtask_status
#         subtasks = SubTask.objects.filter(**filter).order_by('-deadline').all()
#         page_size = SubTaskPaginator()
#         subtasks_paginated = page_size.paginate_queryset(subtasks, request)
#         serializer = SubTaskCreateSerializer(subtasks_paginated, many=True)
#         return page_size.get_paginated_response(serializer.data)
#
#     def post(self,request):
#         serializer = SubTaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class SubTaskDetailUpdateDeleteView(APIView):
#     def get(self, request, pk):
#         subtask = get_object_or_404(SubTask, pk=pk)
#         serializer = SubTaskCreateSerializer(subtask)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         subtask = get_object_or_404(SubTask, pk=pk)
#         serializer = SubTaskCreateSerializer(subtask, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         subtask = get_object_or_404(SubTask, pk=pk)
#         subtask.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class TaskListCreateAPIView(ListCreateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter,
#                        filters.OrderingFilter]
#     filterset_fields = ['status', 'deadline']
#     search_fields = ['title', 'description']
#     ordering_fields = ['created_at']
#
#
# class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#
#
# class SubTaskListCreateAPIView(ListCreateAPIView):
#     queryset = SubTask.objects.all()
#     serializer_class = SubTaskCreateSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter,
#                        filters.OrderingFilter]
#     filterset_fields = ['status', 'deadline']
#     search_fields = ['title', 'description']
#     ordering_fields = ['created_at']
#
#
# class SubTaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
#     queryset = SubTask.objects.all()
#     serializer_class = SubTaskCreateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class=CategoryCreateSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def tasks_count(self, request, pk=None):
        category = self.get_object()
        count_tasks = category.task_set.count()
        return Response({'count': count_tasks})


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, TaskPermission]
    serializer_classes = {
        'list': TaskDetailSerializer,
        'create': TaskCreateSerializer
    }
    default_serializer_class = TaskSerializer


    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def user_tasks(self, request, pk=None):
        tasks = Task.objects.filter(owner=self.request.user).order_by('-created_at')
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)


class SubTaskViewSet(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SubTaskPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['status', 'deadline', 'task']
    search_fields = ['title', 'description', 'task']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        response = Response({'message': 'Successfully logged in'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        response.set_cookie(
            key='refresh_token',
            value=str(refresh_token),
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response


class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        response.delete_cookie(key='access_token')
        response.delete_cookie(key='refresh_token')

        return response

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
