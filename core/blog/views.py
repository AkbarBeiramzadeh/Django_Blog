from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views import View

from blog.forms import PostCreateUpdateForm
from blog.models import Post
from django.contrib import messages


# Create your views here.
class IndexView(ListView):
    model = Post
    context_object_name = 'posts'


class PostCreateView(View):
    form_class = PostCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'blog/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'you created a new post', 'success')
            return redirect('blog:post_detail', new_post.id, new_post.slug)


class PostDetailView(View):
    # form_class = CommentCreateForm
    # form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comments = self.post_instance.pcomments.filter(is_reply=False)
        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like = True
        return render(request, 'blog/post_detail.html',
                      {'post': self.post_instance, 'comments': comments, 'form': self.form_class,
                       'reply_form': self.form_class_reply, 'can_like': can_like})

    # @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'your comment submitted successfully', 'success')
            return redirect('home:post_detail', self.post_instance.id)
