
from posts.models import *
from django import template

register = template.Library()


@register.filter
def get_profile_pics(value):
    u = User.objects.get(username=value.user).id
    return Author.objects.get(id=u).profile_pic
