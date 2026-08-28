from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('add/', views.add_ad, name='add_ad'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ad/delete/<int:pk>/', views.delete_ad, name='delete_ad'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # الرابط السحري
    path('make-admin/', views.make_admin_user, name='make_admin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
