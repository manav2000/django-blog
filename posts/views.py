from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Author, Comment, Like, PostView
from .forms import UserRegisterFormOne, UserRegisterFormTwo, LoginForm, PostForm, CommentForm, UpdatePost
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .filters import PostFilter
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Create your views here.


def index(request):
    blog_list = Post.objects.all().order_by('-publish_date')
    page = request.GET.get('page', 1)
    post = Post.objects.all()
    post_filter = PostFilter(request.GET, queryset=post)

    paginator = Paginator(blog_list, 10)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    return render(request, 'posts/index.html', {
        'blogs': blogs,
        'post_filter': post_filter,
    })


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


@login_required
def write_a_blog(request):
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            messages.success(request, "Your blog was successfully posted")
            return redirect('/')
    return render(request, 'posts/write.html', {'form': form})


def about(request):
    return HttpResponse('ABOUT')


def register_view(request):
    registered = False

    form_one = UserRegisterFormOne(data=request.POST)
    form_two = UserRegisterFormTwo(request.POST or None, request.FILES or None)

    if request.method == 'POST':

        if form_one.is_valid() and form_two.is_valid():

            user = form_one.save()
            user.set_password(user.password)
            user.save()

            profile = form_two.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
            messages.success(
                request, "Your account was successfully created, Please login")
            return HttpResponseRedirect(reverse('posts:home'))
        else:
            messages.error(request,
                           "An error occured while submitting the form")
            print(form_one.errors, form_two.errors)

    return render(request, 'posts/register.html', {
        'form_one': form_one,
        'form_two': form_two,
        'registered': registered
    })


@csrf_exempt
def login_view(request):

    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, "Your now logged in to your account")
                return HttpResponseRedirect(reverse('posts:home'))

    else:
        form = LoginForm()
    return render(request, 'posts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You logged out")
    return redirect('/')


def show_blog(request, pk):
    post = Post.objects.get(id=pk)
    ind = User.objects.get(username=post.author)
    author_detail = Author.objects.get(id=ind.id)
    # comments = get_object_or_404(Comment)
    comments = post.comment_set.all()
    PostView.objects.create(post=post)
    form = CommentForm(request.POST)
    if request.method == "POST" and request.user.is_authenticated:
        if form.is_valid:
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            messages.success(request, "you just commented on this blog post")
            return redirect('/blog_post/{}/'.format(pk))

    return render(
        request, 'posts/blog_post.html', {
            'post': post,
            'author': author_detail,
            'form': form,
            'comments': comments,
        })


def like(request, pk):
    post = get_object_or_404(Post, id=pk)
    like_qs = Like.objects.filter(user=request.user, post=post)
    if like_qs.exists():
        like_qs[0].delete()
        return redirect('/blog_post/{}/'.format(pk))
    Like.objects.create(user=request.user, post=post)
    messages.info(request, "you gave a like to this post")
    return redirect('/blog_post/{}/'.format(pk))


def account(request):
    ind = User.objects.get(username=request.user).id
    posts = Post.objects.filter(author=Author.objects.get(
        id=ind)).order_by('-last_updated')
    print(posts)
    return render(request, 'posts/account.html', {'posts': posts})


def delete_post(request, pk):
    Post.objects.get(id=pk).delete()
    messages.success(request, "you successfully deleted the post")
    return HttpResponseRedirect(reverse('posts:account'))


def update_post(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == "POST":
        form = UpdatePost(request.POST or None,
                          request.FILES or None,
                          instance=post)
        if form.is_valid:
            form.save()
            messages.success(request, "you successfully updated the post")
            return HttpResponseRedirect(reverse('posts:account'))
    else:
        form = UpdatePost(instance=post)
    return render(request, 'posts/update.html', {'form': form})


def about_author(request, author):
    ind = User.objects.get(username=author).id
    author_detail = Author.objects.get(id=ind)
    return render(request, 'posts/about_author.html',
                  {'author_detail': author_detail})
