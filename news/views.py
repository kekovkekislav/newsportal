from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.views import View
from django.core.paginator import Paginator


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
    paginate_by = 1
    form_class = PostForm
    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['category'] = Category.objects.all()
        context['form'] = PostForm()

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

class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    queryset = Post.objects.all()

class PostCreateView(CreateView):
    template_name = 'post_add.html'
    form_class = PostForm

class PostUpdateView(UpdateView):
    template_name = 'post_add.html'
    form_class = PostForm
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
    
class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
