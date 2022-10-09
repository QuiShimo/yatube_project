from django.shortcuts import render


# Create your views here.
def index(request):
    template = 'posts/index.html'
    context = {
        'title': 'Yatube - главная страница',
        'text': 'Это главная страница проекта Yatube',
    }

    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    context = {
        'title': 'Yatube - информация о группах',
        'text': 'Здесь будет информация о группах проекта Yatube',
    }

    return render(request, template, context)
