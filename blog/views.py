from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings


from .models import Post
from .forms import PostForm


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
	Post.objects.get(pk=pk)
	post = get_object_or_404(Post, pk=pk)


	return render(request, mark_safe('blog/post_detail.html'), {'post': post})

def handle_uploaded_file(f):
    destination = open('media/iamge.jpeg', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


def post_new(request):
	if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                #handle_uploaded_file(request.FILES['image'])
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
	else:
	    	form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
