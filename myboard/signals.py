from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Response
from .tasks import send_mail_response 
 
@receiver(post_save, sender=Response)
def send_post(sender, instance, created, **kwargs):
    if created:
        send_mail_response.delay(instance.pk)

@receiver(post_save, sender=User)
def send_post(sender, instance, created, **kwargs):
    if created:
        # Чтобы в редакторе постов можно было загружать файлы
        instance.is_staff = True
        instance.save()
        
