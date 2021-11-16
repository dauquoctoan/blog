from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('', views.index, name='index'),
   path('register/', views.register, name='register'),
   path('adduser/', views.adduser, name='adduser'),
   path('login/', views.loginuser, name="login"),
   path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
   path('auth/', views.authuser, name="auth"),
   path('postbyid/<int:pk>', views.getpostbycategory, name="postbyid"),
   path('post/<int:pk>/', views.post, name='post')
]