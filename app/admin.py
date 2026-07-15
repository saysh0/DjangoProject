from django.contrib import admin
from app.models import Task, SubTask, Category

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'status', 'deadline')
    ordering = ('-created_at', 'status', 'deadline')
    readonly_fields = ('created_at',)

admin.site.register(Task, TaskAdmin)


class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'status', 'deadline', 'task')
    ordering = ('-created_at', 'status', 'deadline')
    readonly_fields = ('created_at', )

admin.site.register(SubTask, SubTaskAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)