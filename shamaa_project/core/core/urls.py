from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_ad, name='add_ad'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('make-admin/', views.make_admin_view, name='make_admin'),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_ad, name='add_ad'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('make-admin/', views.make_admin_view, name='make_admin'),
]
