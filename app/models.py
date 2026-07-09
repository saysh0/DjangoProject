from django.db import models

# Create your models here.
class Choices(models.TextChoices):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    PENDING = 'pending'
    BLOCKED = 'blocked'
    DONE = 'done'


class Category(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=100, unique_for_date='created_at')
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    status = models.CharField(choices=Choices, default=Choices.NEW, max_length=100)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(choices=Choices, default=Choices.NEW, max_length=100)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title