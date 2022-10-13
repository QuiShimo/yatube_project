from django.shortcuts import get_object_or_404, render
from posts.models import Group, Post


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()[:10]
    context = {
        'title': 'Последние обновления на сайте',
        'posts': posts,
    }

    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:10]
    context = {
        'title': f'Записи сообщества {group}',
        'group': group,
        'posts': posts,
    }

    return render(request, template, context)
