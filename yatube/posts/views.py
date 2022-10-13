from django.shortcuts import get_object_or_404, render
from .models import Group, Post


# Create your views here.
def index(request):
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'title': 'Главная страница',
        'posts': posts,
    }

    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'title': 'Yatube - информация о группах',
        'group': group,
        'posts': posts,
    }

    return render(request, template, context)
