from django.urls import path

from .views import (
    ArticleListView,
    ArtilceMyListView,
    ArticleDetailView,
    ArticleEditView,
    ArticleDeleteView,
    ArticleCreateView,
)

urlpatterns = [
    path("", ArticleListView.as_view(), name="home"),
    path("", ArticleListView.as_view(), name="article_list"),
    path("my/", ArtilceMyListView.as_view(), name="article_my_list"),
    path("<int:pk>/detail/", ArticleDetailView.as_view(), name="article_detail"),
    path("<int:pk>/edit/", ArticleEditView.as_view(), name="article_edit"),
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name="article_delete"),
    path("create/", ArticleCreateView.as_view(), name="article_create"),
]
