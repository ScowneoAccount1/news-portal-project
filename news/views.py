from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import SearchFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render


class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = "posts"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        context['is_author'] = self.request.user.groups.filter(name='author').exists()
        context['is_auth'] = self.request.user.is_authenticated
        context['current_user'] = self.request.user
        return context


class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = "posts"

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = SearchFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class AddList(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'add.html'
    form_class = PostForm
    permission_required = ('news.add_post',)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'edit.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


@login_required
def subscribe_categories(request):
    user = request.user
    catt_id = request.POST['catt_id']
    category = Category.objects.get(pk=int(catt_id))

    if user not in category.subscr_user.all():
        category.subscr_user.add(user)

    else:
        category.subscr_user.remove(user)

    return redirect(request.META.get('HTTP_REFERER', '/'))
