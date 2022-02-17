from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField 


class Post(models.Model):
    TYPE = (
        ('tanks', 'Танки'),
        ('heals', 'Хилы'),
        ('dd', 'ДД'),
        ('traders', 'Торговцы'),
        ('guildmasters', 'Гилдмастеры'),
        ('questgivers', 'Квестгиверы'),
        ('farriers', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potionmakers', 'Зельевары'),
        ('spellmasters', 'Мастера заклинаний'),
    )
    date = models.DateTimeField(verbose_name='Дата', default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = RichTextUploadingField()
    category = models.CharField(max_length=12, choices=TYPE, default='tanks')

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk' : self.pk})
    
    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

class Response(models.Model):
    date = models.DateTimeField(verbose_name='Дата', default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.BooleanField(default=False) # Принят/Не принят отклик от др. пользователя

    def get_absolute_url(self):
        return reverse('response_detail', kwargs={'pk' : self.pk})

    def __str__(self):
        return f'{self.author} {self.post} {self.text}'
    
    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'