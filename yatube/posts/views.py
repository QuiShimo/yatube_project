from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from posts.models import Group, Post


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'title': 'Последние обновления на сайте',
        'page_obj': page_obj,
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


def profile(request, username):
    user = User.objects.get(username=username)
    post_list = Post.objects.filter(author=user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    post_count = post_list.count()

    context = {
        'page_obj': page_obj,
        'posts_count': post_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    post_count = Post.objects.filter(author=post.author).count()

    context = {
        'posts_count': post_count,
        'post': post,
    }

    return render(request, 'posts/post_detail.html', context)
