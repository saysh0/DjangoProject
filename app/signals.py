from django.db.models.signals import post_save
from django.dispatch import receiver
from.models import Task
from django.core.mail import send_mail

@receiver(post_save, sender=Task)
def task_status_changed(sender, instance, created, **kwargs):
    print("Сигнал сработал!")
    if created:
        return
    if instance.status != instance._original_status:
        if instance.owner and instance.owner.email:
            send_mail(
                subject='Изменения статуса задачи',
                message='Статус вашей задачи был изменен',
                from_email='from@example.com',
                recipient_list=[instance.owner.email],
            )
