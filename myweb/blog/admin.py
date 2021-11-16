from django.contrib import admin
from . import models

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title']
    list_filter = ['title']


class CommentInLine(admin.TabularInline):
    model = models.Comment


class ContentInLine(admin.StackedInline):
    model = models.Content


class PostAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'date']
    list_filter = ['title']
    inlines = [ContentInLine, CommentInLine]


admin.site.register(models.PostCategory, CategoryAdmin)
admin.site.register(models.Post, PostAdmin)

