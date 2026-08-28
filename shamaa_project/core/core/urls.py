from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_ad, name='add_ad'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('make-admin/', views.make_admin_view, name='make_admin'),
]
