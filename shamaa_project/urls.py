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
    from core.views import make_admin_view  # تأكد من استيراد الدالة في الأعلى
path('add/', views.add_ad, name='add_ad'),
# وفي داخل urlpatterns أضف هذا السطر:
path('make-admin/', make_admin_view, name='make_admin'),
    # الرابط السحري
    path('make-admin/', views.make_admin_user, name='make_admin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    # النظام واللوحة
    path('admin/', admin.site.urls),
    path('make-admin/', views.make_admin_user, name='make_admin'), # الرابط السحري
    
    # الصفحات الرئيسية
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # إدارة الإعلانات
    # path('add/', views.add_ad, name='add_ad'), # فعلها بعد عمل فورم الإضافة
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('ad/<int:pk>/delete/', views.delete_ad, name='delete_ad'),
    
    # نظام الحسابات (جاهز للربط مع قوالبك)
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

# تفعيل ظهور الصور المرفوعة على سيرفرات Render
if settings.DEBUG or not settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_ad, name='add_ad'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('make-admin/', views.make_admin_view, name='make_admin'),
]
