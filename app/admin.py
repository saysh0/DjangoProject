from django.contrib import admin
from app.models import Task, SubTask, Category, Choices


# Register your models here.

class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'task', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'status', 'deadline', 'task')
    ordering = ('-created_at', 'status', 'deadline')
    readonly_fields = ('created_at', )
    actions = ['mark_as_done']

    def mark_as_done(self, request, queryset):
        queryset.update(status=Choices.DONE)

    mark_as_done.short_description = 'Mark selected tasks as done'

admin.site.register(SubTask, SubTaskAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)

class SubTaskInLine(admin.StackedInline):
    model = SubTask
    extra = 1

class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'description', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'deadline')
    search_fields = ('title', 'status', 'deadline')
    ordering = ('-created_at', 'status', 'deadline')
    readonly_fields = ('created_at',)
    inlines = [SubTaskInLine]

    def short_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10] + '...'
        return obj.title

admin.site.register(Task, TaskAdmin)
