from django.contrib import admin
from .models import PostView, Author, Post, Like, Comment

# Register your models here.


admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostView)
admin.site.register(Like)
