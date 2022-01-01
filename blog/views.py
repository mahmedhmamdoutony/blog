
from django.core import paginator
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from .models import Comment, Post
from .forms import CommentForm
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import CreateView, UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


def blog_home(request):
    post = Post.objects.all()
    pagintor = Paginator(post, 2)
    page = request.GET.get('page')
    try:
        post = pagintor.page(page)
    except PageNotAnInteger:
        post = pagintor.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_page)
    comment = Comment.objects.all()
    sub = Post.objects.all()
    context = {'posts': post, 'comments': comment, 'sub': sub }
    return render(request, 'blog/index.html', context)


def blog_details(request, blog_id):
    new_comment = CommentForm(request.POST)
    post = get_object_or_404(Post, id=blog_id)
    comment = post.comments.filter(is_active=True)
    if request.method == 'POST':
        new_comment = CommentForm(data=request.POST)
        if new_comment.is_valid():
            new_comment = new_comment.save(commit=False)
            new_comment.comment = post
            new_comment.is_active = False
            new_comment.save()
            messages.success(
                request, 'success send comment , it will be show up as soon as possible')
            return redirect('blog:blog_home')
        else:
            new_comment = CommentForm(request.POST)

    context = {'posts': post, 'comments': comment, 'form': new_comment}
    return render(request, 'blog/blog_details.html', context)


def comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    context = {'comments': comment}
    return render(request, 'blog/comment_details.html', context)


def comment_all(request, com_id):
    post = get_object_or_404(Post, id=com_id)
    comment = Comment.objects.filter(comment__id=com_id)
    paginator = Paginator(comment,2)
    page = request.GET.get('page')
    try:
        comment = paginator.page(page)
    except PageNotAnInteger:
        comment = paginator.page(1)
    except EmptyPage:
        comment = paginator.page(paginator.num_page)        
    context = {'comments': comment, 'post': post}
    return render(request, 'blog/comment_all.html', context)


class NewPost(LoginRequiredMixin,CreateView):
    model=Post
    fields = ['title', 'content', 'photo']
    template_name ='blog/new_post.html'

    def form_valid(self,form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class UpdatePost(UserPassesTestMixin,LoginRequiredMixin, UpdateView):
    model=Post
    fields = ['title', 'content', 'photo']
    template_name ='blog/update_post.html'

    def form_valid(self,form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.created_by:
            return True
        else:
            return False    

class DeletePost(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    model = Post 
    success_url ='/'
    def test_func(self) :
        post = self.get_object()
        if self.request.user == post.created_by:
            return True
        return False            