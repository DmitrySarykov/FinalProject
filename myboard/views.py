from urllib import request, response
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


from .filters import SearchFilter
from .models import *
from .forms import *
from .tasks import send_mail_status


# Объявления
class PostListView(ListView):
    model = Post  
    template_name = 'post_list.html' 
    context_object_name = 'post_list'
    ordering = ['-date']
    paginate_by = 10
    queryset = Post.objects.order_by('-date')

class PostCreateView(LoginRequiredMixin,CreateView):
    template_name = 'post_edit.html'
    form_class = PostForm

    def get_initial(self):
        return {
            'author': self.request.user,
        }

class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post  
    template_name = 'post_detail.html' 
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["response"] = Response.objects.all().filter(post__pk = self.kwargs["pk"])
        return context
       
class PostUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'post_edit.html'
    form_class = PostForm
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class PostDeleteView(LoginRequiredMixin,DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('post_list')
    context_object_name = 'post'

# Отклики
class ResponseCreateView(LoginRequiredMixin,CreateView):
    template_name = 'response_add.html'
    form_class = ResponseForm
    success_url = reverse_lazy('post_list')

    def get_initial(self):
        return {
            'post': self.kwargs['pk'],
            'author': self.request.user,
        }

@login_required
def ChangeStatus(request, *args, **kwargs):
    pk = kwargs.get('pk')
    response = Response.objects.get(pk=pk)
    response.status = not response.status
    response.save()
    if response.status: 
        send_mail_status.delay(response.pk)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ResponseDeleteView(LoginRequiredMixin,DeleteView):
    template_name = 'response_delete.html'
    success_url = reverse_lazy('post_list')
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Response.objects.get(pk=id)
    
# Страница пользователя
class AuthorView(LoginRequiredMixin,ListView):
    model = User  
    template_name = 'author_page.html' 
    context_object_name = 'author'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = Post.objects.all().filter(author__pk = self.kwargs["pk"])
        context["response"] = Response.objects.all().filter(post__author__pk = self.kwargs["pk"])
        context['filter'] = SearchFilter(self.request.GET, queryset=context["response"])
        return context