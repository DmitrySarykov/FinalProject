from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth

from .views import *

urlpatterns = [
    # Объявления
    path('', PostListView.as_view(), name="post_list"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post_detail"),
    path('post/add/', PostCreateView.as_view(), name="post_add"),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    # Отклики
    path('response/<int:pk>/create/', ResponseCreateView.as_view(), name="response_add"),
    path('response/<int:pk>/delete/', ResponseDeleteView.as_view(), name='response_delete'),
    path('response/<int:pk>/status/', ChangeStatus, name='response_status'),
    # Страница пользователя
    path('author/<int:pk>', AuthorView.as_view(), name="author_page"),
]
