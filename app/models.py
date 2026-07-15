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


    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        constraints = [models.UniqueConstraint(fields=['name'], name='unique_name_category')]
        verbose_name_plural = 'Categories'

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    status = models.CharField(choices=Choices, default=Choices.NEW, max_length=100)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        constraints = [models.UniqueConstraint(fields=['title'], name='unique_title_task')]
        verbose_name_plural = 'Tasks'


class SubTask(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.CharField(choices=Choices, default=Choices.NEW, max_length=100)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        constraints = [models.UniqueConstraint(fields=['title'], name='unique_title_subtask')]
        verbose_name_plural = 'Subtasks'