import django
import os
from datetime import datetime, timedelta
from django.db.models import F

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')
django.setup()

from app.models import *

new_Task = Task(
    title = "Prepare presentation",
    description = "Prepare materials and slides for the presentation",
    status = Choices.NEW,
    deadline = datetime.now() + timedelta(days=3)
)
new_Task.save()
print(f"Task created: {new_Task.title}")

new_SubTask = SubTask(
    title = "Gather information",
    description = "Find necessary information for the presentation",
    task = Task.objects.get(title="Prepare presentation"),
    status = Choices.NEW,
    deadline = datetime.now() + timedelta(days=2)
)
new_SubTask.save()

new_SubSubTask_2 = SubTask(
    title = "Create slides",
    description = "Create presentation slides",
    task = Task.objects.get(title='Prepare presentation'),
    status = Choices.NEW,
    deadline = datetime.now() + timedelta(days=1)
)
new_SubSubTask_2.save()


all_Task_status_New = Task.objects.all().filter(status=Choices.NEW)
all_SubTask_status_New = SubTask.objects.all().filter(status=Choices.DONE, deadline__lte=datetime.now())

for tasks in all_Task_status_New:
    print(tasks)

for subtasks in all_SubTask_status_New:
    print(subtasks)

update_Task_Prepare_presentation = Task.objects.get(title="Prepare presentation")
update_Task_Prepare_presentation.status = Choices.IN_PROGRESS
update_Task_Prepare_presentation.save()

SubTask.objects.filter(title="Gather information").update(deadline=F("deadline") - timedelta(days=2))

update_SubTask_Create_slides = SubTask.objects.get(title="Create slides")
update_SubTask_Create_slides.description = "Create and format presentation slides"
update_SubTask_Create_slides.save()

Task.objects.filter(title="Prepare presentation").delete()