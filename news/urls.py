from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail,PostSearch,CreateNew,PostDeleteView,UpdateNew
from django.contrib.auth.decorators import login_required




urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view()), 
   path('<int:pk>', PostDetail.as_view(),name ='post_detail'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('create/', CreateNew.as_view(), name='create_new'),
   path('<int:pk>/edit', UpdateNew.as_view(), name='post_update'),
   path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),

]