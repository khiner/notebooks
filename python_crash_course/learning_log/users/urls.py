from django.urls import path
from django.contrib.auth.views import login, logout

from . import views

urlpatterns = [
    # Login page
    path('login', login, {'template_name': 'users/login.html'}, name='login'),
    # Logout page
    path('logout', views.logout_view, name='logout'),
    # Registration page
    path('register', views.register, name='register'),
]
