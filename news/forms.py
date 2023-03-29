from django.forms import ModelForm
from .models import Post
from django import forms
 
 
# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        widgets = {'text':forms.Textarea(attrs={'rows':1,'cols':15})}
        fields = ['title', 'author','text']