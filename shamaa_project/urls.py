from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, add_ad, ad_detail, dashboard_view, delete_ad, register_view, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('add/', add_ad, name='add_ad'),
    path('ad/<int:pk>/', ad_detail, name='ad_detail'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('ad/delete/<int:pk>/', delete_ad, name='delete_ad'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)