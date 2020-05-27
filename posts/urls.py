from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.index, name='home'),
    path('write/', views.write_a_blog, name='write_blog'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('blog_post/<int:pk>/', views.show_blog, name='blog_post'),
    path('register/', views.register_view, name='register'),
    path('like/<int:pk>/', views.like, name='like'),
    path('account/', views.account, name='account'),
    path('account/delete_post/<int:pk>/',
         views.delete_post, name='delete_post'),
    path('account/update_post/<int:pk>/',
         views.update_post, name='update_post'),
    path('about_author/<str:author>/', views.about_author, name='about_author')
]
