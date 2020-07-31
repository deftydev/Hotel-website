from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from accounts import views
from products import views as vw
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('home/', views.home1 , name='home1'),
    path('',vw.HomePageView.as_view(), name='home'),
    path('accounts/signup', views.SignUpView.as_view(), name='signup'),
    path('accounts/signup/customer/', views.CustomerSignUpView.as_view(), name='customer_signup'),
    path('accounts/signup/admin/', views.AdminSignUpView.as_view(), name='admin_signup'),
    path('products/', include('products.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
