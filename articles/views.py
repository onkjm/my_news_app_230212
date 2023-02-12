from django.shortcuts import render
from django.views.generic import (
    View,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy, reverse

from .models import Article
from .forms import CommentForm


# Create your views here.
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    paginate_by = 100  # if pagination is desired
    template_name = "article_list.html"


class ArtilceMyListView(ArticleListView):
    template_name = "article_mylist.html"


class CommentGet(DetailView):
    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["commentform"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = CommentForm
    template_name = "article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.article = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.get_object()
        return reverse("article_detail", kwargs={"pk": article.pk})


class ArticleDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)


class ArticleEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = "article_update.html"
    fields = [
        "title",
        "body",
    ]

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "article_delete.html"
    success_url = reverse_lazy("article_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


# class ArticleCreateView(LoginRequiredMixin, CreateView):
class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    permission_required = "polls.add_choice"

    model = Article
    template_name = "article_create.html"
    fields = [
        "title",
        "body",
        # "author",
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff
