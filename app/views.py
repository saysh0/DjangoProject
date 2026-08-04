from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .models import *
from.serializers import TaskSerializer
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

@api_view(['GET'])
def get_tasks(request):
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

