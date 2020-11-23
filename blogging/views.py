from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.template import loader
from blogging.models import Post
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blogging.forms import NewPost
from django.utils import timezone


class BlogListView(ListView):
    published = Post.objects.exclude(published_date__exact=None)
    queryset = published.order_by("-published_date")
    template_name = "blogging/list.html"


class BlogDetailView(DetailView):
    queryset = Post.objects.exclude(published_date__exact=None)
    template_name = "blogging/detail.html"


def add_model(request):
    if request.method == "POST":
        form = NewPost(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            if User.objects.filter(username=model_instance.author).exists():
                new_author = User.objects.get(username=model_instance.author)
            else:
                new_author = User.objects.create_user(model_instance.author)
            newpost = Post(
                title=model_instance.title,
                text=model_instance.text,
                author=new_author,
                created_date=model_instance.timestamp,
                modified_date=model_instance.timestamp,
                published_date=model_instance.timestamp,
            )
            newpost.save()
            return redirect("/")

    else:
        form = NewPost()
        return render(request, "blogging/add.html", {"form": form})


# def detail_view(request, post_id):
#     published = Post.objects.exclude(published_date__exact=None)
#     try:
#         post = published.get(pk=post_id)
#     except Post.DoesNotExist:
#         raise Http404
#     context = {'post': post}
#     return render(request, 'blogging/detail.html', context)
#
#
# def list_view(request):
#     published = Post.objects.exclude(published_date__exact=None)
#     posts = published.order_by('-published_date')
#     context = {'posts': posts}
#     return render(request, 'blogging/list.html', context)
