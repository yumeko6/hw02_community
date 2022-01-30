from django.shortcuts import render, get_object_or_404
from .models import Post, Group


LAST_POSTS = 10


def index(request):
    posts = Post.objects.all()[:LAST_POSTS]
    context = {
        'posts': posts,
        'title': 'Последние обновления на сайте',
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).all()[:LAST_POSTS]
    context = {
        'group': group,
        'posts': posts,
        'title': f'Записи сообщества {group.title}',
    }

    return render(request, 'posts/group_list.html', context)
