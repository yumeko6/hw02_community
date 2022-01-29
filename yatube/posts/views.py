from django.shortcuts import render, get_object_or_404
from .models import Post, Group


last_posts = 10


def index(request):
    posts = Post.objects.all()[:last_posts]
    context = {
        'posts': posts,
        'title': 'Последние обновления на сайте',
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).all()[:last_posts]
    context = {
        'group': group,
        'posts': posts,
        'title': f'Записи сообщества {group.title}',
    }

    return render(request, 'posts/group_list.html', context)
