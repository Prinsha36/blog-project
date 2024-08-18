from typing import Any
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.utils import timezone

from blog_app.models import Post

from blog_app.forms import PostForm

from django.views.generic import ListView, DetailView, CreateView, UpdateView,View

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


# Create your views here.

# class based views


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"

    def get_queryset(self) -> QuerySet[Any]:
        posts = Post.objects.filter(published_at__isnull=False)
        return posts


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        queryset = Post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=False)
        return queryset


# @login_required
# def post_delete(request, pk):
#     post = Post.objects.get(pk=pk)
#     post.delete()
#     return redirect("post-list")

class PostDeleteView(LoginRequiredMixin,View):
    def get(self, request,pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect("post-list")
    



class DraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "draft_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        queryset = Post.objects.filter(published_at__isnull=True)
        return queryset


# @login_required
# def draft_list(request):
# post = Post.objects.filter(published_at__isnull=True)
# return render(request, "draft_list.html", {"posts": post})


# @login_required
# def draft_detail(request, pk):
#     post = Post.objects.get(pk=pk, published_at__isnull=True)
#     return render(request, "draft_detail.html", {"post": post})


class DraftDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "draft_detail.html"
    context_object_name = "post"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = Post.objects.filter(pk=self.kwargs["pk"], published_at__isnull=True)
        return queryset


# @login_required
# def post_create(request):
#     form = PostForm()
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect("draft-detail", pk=post.pk)
#     return render(request, "post_create.html", {"form": form})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "post_create.html"
    form_class = PostForm
    success_url = reverse_lazy("post-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# @login_required
# def draft_publish(request, pk):
#     post = Post.objects.get(pk=pk, published_at__isnull=True)
#     post.published_at = timezone.now()
#     post.save()
#     return redirect("post-list")


class DraftPublishView(LoginRequiredMixin,View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk, published_at__isnull=True)
        post.published_at = timezone.now()
        post.save()
        return redirect("post-list")


# @login_required
# def post_update(request, pk):
#     post = Post.objects.get(pk=pk)
#     form = PostForm(instance=post)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save()
#             if post.published_at:
#                 return redirect("post-detail", post.pk)
#             else:
#                 return redirect("draft-detail", post.pk)
#     return render(
#         request,
#         "post_create.html",
#         {"form": form},
#     )


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "post_create.html"
    form_class = PostForm

    def get_success_url(self):
        post = self.get_object()
        if post.published_at:
            return reverse_lazy("post-detail", kwargs={"pk": post.pk})
        else:
            return reverse_lazy("draft-detail", kwargs={"pk": post.pk})
