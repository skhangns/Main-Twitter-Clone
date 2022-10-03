from django import forms
from django.forms.fields import ImageField
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from .forms import PostForm
# Create your views here.


def index(request):
    # If the method is post
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        # if the mrthod is valid
        if form.is_valid():
            #Yes, Save
            form.save()
            print("hello its valid")

            # Redirect to home
            return HttpResponseRedirect('/')

        else:
            # No, Show Error
            print("its not valid")
            return HttpResponseRedirect(form.errors.as_json())

    # Get all posts,limit = 20
    posts = Post.objects.all().order_by('-created_at')[:20]
    form = PostForm()
    # Show
    return render(request, 'posts.html', {'posts': posts})


def likes(request, id):
    print(id)
    likedtweet = Post.objects.get(id=id)
    likedtweet.like_count += 1
    likedtweet.save()
    return HttpResponseRedirect("/")


def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/')


def edit(request, id):
    if request.method == "GET":
        posts = Post.objects.get(id=id)
        return render(request, "edit.html", {"posts": posts})
    if request.method == "POST":
        editposts = Post.objects.get(id=id)
        form = PostForm(request.POST, request.FILES, instance=editposts)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        else:
            return HttpResponse("not valid")
