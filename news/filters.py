from django_filters import FilterSet, DateFilter
from .models import Post
from django.forms import DateInput


# создаём фильтр
class PostFilter(FilterSet):
    date = DateFilter(field_name='created', widget=DateInput(attrs={'type': 'date'}), label='Искать по дате:',
                      lookup_expr='date__gte')
    class Meta:
        model = Post
        fields = {

            'title': ['icontains'],

            'author': ['exact'],

        }