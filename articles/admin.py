from django.contrib import admin
from .models import Article, Comment

# Register your models here.


# class CommentInline(admin.StackedInline):
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0  # the numbers of empty rows to display (if not spesified, 3.)


class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
