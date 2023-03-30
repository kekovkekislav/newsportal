from django.contrib.auth.models import User,Group
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



# Create your views here.
class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required(login_url='accounts/signup')
def become_author(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('/')