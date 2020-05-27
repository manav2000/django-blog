import django_filters
from .models import *


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title', lookup_expr='icontains')

    class Meta():
        model = Post
        fields = ['title', ]


PostFilter.base_filters['title'].label = ''
