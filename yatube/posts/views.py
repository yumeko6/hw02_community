from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import truncatewords
from django.utils.timezone import localtime

from .forms import PostForm
from .models import Post, Group, User


def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'title': 'Последние обновления на сайте',
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'page_obj': page_obj,
        'title': f'Записи сообщества {group.title}',
    }

    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    post_author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=post_author).all().order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    count = Post.objects.filter(author=post_author).count()
    context = {
        'username': post_author,
        'title': f'Профайл пользователя {post_author}',
        'page_obj': page_obj,
        'count': count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    count = Post.objects.count()
    context = {
        'post': post,
        'title': f'Пост {truncatewords(post.text, 30)}',
        'count': count,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pub_date = localtime()
            post.save()
            return redirect(f'/profile/{request.user}/')
        else:
            form = PostForm()
    context = {
        'form': form,
        'title': 'Новый пост',
    }
    return render(request, 'posts/create_post.html', context)
