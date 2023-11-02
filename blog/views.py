from django.views.generic import ListView, DetailView

from .models import Post


class BlogList(ListView):
    model = Post
    ordering = '-create_ts'
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
