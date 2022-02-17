from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from datetime import date, timedelta 
from .models import Post, Response,User

@shared_task
def send_mail_response(response_pk):
    response = Response.objects.get(pk=response_pk)
    user = response.post.author
    site = Site.objects.get_current()
    print(f'Отправка письма {user.email}')
    msg = EmailMultiAlternatives(subject=response.post.title,to=[user.email])
    html_content = render_to_string('mess_new_response.html',{'response':response,'user':user,'site':site})
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def send_mail_status(response_pk):
    response = Response.objects.get(pk=response_pk)
    user = response.post.author
    site = Site.objects.get_current()
    print(f'Отправка письма {response.author.email}')
    msg = EmailMultiAlternatives(subject=response.text,to=[response.author.email])
    html_content = render_to_string('mess_response_status.html',{'response':response,'user':user,'site':site})
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# Рассылка еженедельных новостей 
@shared_task
def send_week_news():
    today = date.today()
    list_email = User.objects.exclude(email='').values_list('email',flat=True)
    if list_email :
        site = Site.objects.get_current()
        last_week = today - timedelta(days=7)
        posts=Post.objects.filter(date__range=[last_week,today]).order_by('date')
        print(f'Новости за неделю {list_email}')
        msg = EmailMultiAlternatives(
            subject='Новости за неделю',
            to=list_email, 
        )
        html_content = render_to_string('mess_posts_week.html',{'posts_list':posts,'site':site})
        msg.attach_alternative(html_content, "text/html")
        msg.send()
