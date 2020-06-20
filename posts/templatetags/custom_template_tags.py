from posts.models import *
from django import template
from django.db.models import Count
from taggit.models import Tag
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.filter
def get_profile_pics(value):
    u = User.objects.get(username=value.user).id
    return Author.objects.get(id=u).profile_pic

@register.inclusion_tag('most_liked_posts.html')
def get_most_liked_posts(count=5):
    most_liked_posts = Post.objects.annotate(total_likes=Count('like')).order_by('-total_likes')[:count]
    return {'most_liked_posts': most_liked_posts}

@register.inclusion_tag('tags.html')
def get_tags(count=50):
    tags = Tag.objects.all()[:count]
    return {'tags': tags}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
