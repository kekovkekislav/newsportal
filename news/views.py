from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


#basic user - asfkjasdf
#premium user - jfdhsgkj
#test_basicuser@mail.ru - asfkasdf


from .filters import PostFilter
from .models import Post,Category
from .forms import PostForm


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'text'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10
    form_class = PostForm
 
    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context
    

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class CreateNew(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = '/accounts/signup/'
    template_name = 'new_edit.html'
    form_class = PostForm
    model = Post
    permission_required = 'news.add_post'
 
class CreateArticle(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    login_url = '/accounts/signup/'
    template_name = 'article_edit.html'
    model = Post
    form_class = PostForm
    permission_required = 'news.add_post'




class UpdateNew(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/accounts/signup/'
    template_name = 'new_edit.html'
    form_class = PostForm
    model = Post
    permission_required = 'news.change_post'




class UpdateArticle(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    login_url = '/accounts/signup/'
    template_name = 'article_edit.html'
    form_class = PostForm
    model = Post
    permission_required = 'news.change_post'


    
class PostDeleteView(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    login_url = '/accounts/signup/'
    template_name = 'new_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    model = Post
    permission_required = 'news.delete_post'
