from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import *
from.serializers import *
# Create your views here.

from django.http import HttpResponse

def hello(request):
    return HttpResponse('Hello, Nikita.')

@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

DAYS = {
    'sunday': 1,
    'monday': 2,
    'tuesday': 3,
    'wednesday': 4,
    'thursday': 5,
    'friday': 6,
    'saturday': 7,
}

@api_view(['GET'])
def get_tasks(request):
    day_of_week = request.query_params.get('day_of_week')
    if day_of_week:
        number_day_of_week = DAYS.get(day_of_week)
        tasks = Task.objects.filter(deadline__week_day=number_day_of_week)
    else:
        tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    serializer = TaskSerializer(task)
    return Response(serializer.data)

@api_view(['GET'])
def task_stats(request):
    tasks_count = Task.objects.all().count()
    tasks_by_status_count = {}
    for choice in Choices:
        tasks_by_status_count[choice.value] = Task.objects.filter(status=choice).count()
    overdue_tasks_count = Task.objects.filter(deadline__lt=timezone.now()).count()
    return Response({'total': tasks_count, 'by_status': tasks_by_status_count, 'overdue': overdue_tasks_count})

class SubTaskPaginator(PageNumberPagination):
    page_size = 5
class SubTaskListCreateView(APIView):
    def get(self,request):
        filter = {}
        task = request.query_params.get('task')
        subtask_status = request.query_params.get('subtask_status')
        if task:
            filter['task__title'] = task
        if subtask_status:
            filter['status__iexact'] = subtask_status
        subtasks = SubTask.objects.filter(**filter).order_by('-deadline').all()
        page_size = SubTaskPaginator()
        subtasks_paginated = page_size.paginate_queryset(subtasks, request)
        serializer = SubTaskCreateSerializer(subtasks_paginated, many=True)
        return page_size.get_paginated_response(serializer.data)

    def post(self,request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
