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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_ad, name='add_ad'),
    path('edit/<int:pk>/', views.edit_ad, name='edit_ad'),
    path('delete/<int:pk>/', views.delete_ad, name='delete_ad'),
    path('register/', views.register_view, name='register'),
    path('make-admin/', views.make_admin_view, name='make_admin'),
]
from django.urls import path
from . import views

urlpatterns = [
    # الصفحات الرئيسية
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # إدارة الإعلانات
    path('add/', views.add_ad, name='add_ad'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('edit/<int:pk>/', views.edit_ad, name='edit_ad'),
    path('delete/<int:pk>/', views.delete_ad, name='delete_ad'),
    
    # الحسابات والذكاء الاصطناعي
    path('register/', views.register_view, name='register'),
    path('make-admin/', views.make_admin_view, name='make_admin'),
    path('ai-generate/', views.ai_generate_description, name='ai_generate'), # مسار الذكاء الاصطناعي الجديد
]
