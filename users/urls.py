from django.urls import path
from django.contrib.auth import views as auth_views
from .views import logout_user
#users\templates\users\login.html
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', logout_user, name='logout'),
]
