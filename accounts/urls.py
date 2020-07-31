from django.urls import include, path

from . import views

urlpatterns = [
    path('logout', views.logout ,name='logout'),
    path('login', views.login ,name='login'),
]
