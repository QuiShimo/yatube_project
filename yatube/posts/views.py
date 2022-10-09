from django.http import HttpResponse
from django.template import loader


# Create your views here.
def index(request):
    template = loader.get_template('posts/index.html')
    return HttpResponse(template.render({}, request))


def group_posts(request, slug):
    return HttpResponse(f'Посты группы {slug}')
