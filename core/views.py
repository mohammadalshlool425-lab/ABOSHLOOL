from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Ad

@login_required(login_url='login')
def dashboard(request):
    user = request.user
    user_ads = Ad.objects.filter(user=user)
    total_ads_count = user_ads.count()

    search_query = request.GET.get('search', '')
    if search_query:
        user_ads = user_ads.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    sort_by = request.GET.get('sort', '-created_at') 
    valid_sorts = ['price', '-price', 'created_at', '-created_at']
    if sort_by in valid_sorts:
        user_ads = user_ads.order_by(sort_by)

    paginator = Paginator(user_ads, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'user': user,
        'total_ads_count': total_ads_count,
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'core/dashboard.html', context)
    from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Ad, Category
# من المفترض أن يكون لديك ملف forms.py يحتوي على AdForm
# from .forms import AdForm 

def home(request):
    """الصفحة الرئيسية: تعرض أحدث الإعلانات النشطة"""
    latest_ads = Ad.objects.filter(is_active=True)[:12]
    categories = Category.objects.all()
    return render(request, 'core/home.html', {'ads': latest_ads, 'categories': categories})

def ad_detail(request, pk):
    """صفحة تفاصيل الإعلان الواحد"""
    ad = get_object_or_404(Ad, pk=pk, is_active=True)
    
    # زيادة عدد المشاهدات بذكاء
    ad.views_count += 1
    ad.save(update_fields=['views_count'])
    
    return render(request, 'core/ad_detail.html', {'ad': ad})

@login_required(login_url='login')
def dashboard(request):
    """لوحة التحكم الاحترافية للمعلن"""
    user_ads = Ad.objects.filter(user=request.user)
    
    # محرك البحث داخل اللوحة
    search_query = request.GET.get('search', '')
    if search_query:
        user_ads = user_ads.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    # تقسيم الصفحات
    paginator = Paginator(user_ads, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'total_ads': user_ads.count(),
        'total_views': sum(ad.views_count for ad in user_ads), # إجمالي مشاهدات كل إعلاناته
        'page_obj': page_obj,
    }
    return render(request, 'core/dashboard.html', context)

@login_required(login_url='login')
def delete_ad(request, pk):
    """حذف الإعلان مع حماية قوية (فقط صاحب الإعلان يقدر يحذفه)"""
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    if request.method == 'POST':
        ad.delete()
        messages.success(request, "تم حذف الإعلان بنجاح!")
        return redirect('dashboard')
    return render(request, 'core/confirm_delete.html', {'ad': ad})

# ملاحظة: دالة add_ad تعتمد على وجود ملف forms.py لإنشاء النموذج.
from django.shortcuts import redirect # تأكد إنها موجودة فوق مع باقي الاستدعاءات

@login_required(login_url='login')
def add_ad(request):
    """دالة احترافية لإضافة إعلان جديد مع دعم رفع الصور والأقسام"""
    categories = Category.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image') # لاستقبال الصور

        # التأكد من إدخال البيانات الأساسية
        if title and description and price:
            category = Category.objects.filter(id=category_id).first() if category_id else None
            
            # إنشاء الإعلان وحفظه في قاعدة البيانات
            Ad.objects.create(
                user=request.user,
                category=category,
                title=title,
                description=description,
                price=price,
                image=image
            )
            messages.success(request, "تم نشر إعلانك بنجاح! 🚀")
            return redirect('dashboard')
            
        else:
            messages.error(request, "يرجى تعبئة جميع الحقول المطلوبة.")

    # إذا كان الطلب عادي (GET)، اعرض صفحة الإضافة
    return render(request, 'core/add_ad.html', {'categories': categories})
    from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Ad, Category

# ==========================================
# 1. نظام الحسابات (التسجيل، الدخول، الخروج)
# ==========================================
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def make_admin_user(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', '12345678')
        return HttpResponse('<h2 dir="rtl" style="text-align:center; color:green;">تم إنشاء حساب المدير بنجاح!</h2>')
    return HttpResponse('<h2 dir="rtl" style="text-align:center; color:blue;">حساب المدير موجود مسبقاً.</h2>')

# ==========================================
# 2. نظام الإعلانات ولوحة التحكم
# ==========================================
def home(request):
    latest_ads = Ad.objects.filter(is_active=True)[:12]
    categories = Category.objects.all()
    return render(request, 'core/home.html', {'ads': latest_ads, 'categories': categories})

def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk, is_active=True)
    ad.views_count += 1
    ad.save(update_fields=['views_count'])
    return render(request, 'core/ad_detail.html', {'ad': ad})

@login_required(login_url='login')
def dashboard(request):
    user_ads = Ad.objects.filter(user=request.user)
    search_query = request.GET.get('search', '')
    
    if search_query:
        user_ads = user_ads.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    
    paginator = Paginator(user_ads, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'total_ads': user_ads.count(),
        'total_views': sum(ad.views_count for ad in user_ads),
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'core/dashboard.html', context)

@login_required(login_url='login')
def add_ad(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        
        if title and description and price:
            category = Category.objects.filter(id=category_id).first() if category_id else None
            Ad.objects.create(user=request.user, category=category, title=title, description=description, price=price, image=image)
            messages.success(request, "تم نشر إعلانك بنجاح! 🚀")
            return redirect('dashboard')
            
    return render(request, 'core/add_ad.html', {'categories': categories})

@login_required(login_url='login')
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    if request.method == 'POST':
        ad.delete()
        messages.success(request, "تم الحذف بنجاح!")
        return redirect('dashboard')
    return render(request, 'core/confirm_delete.html', {'ad': ad})
    from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Ad, Category

# ==========================================
# 1. نظام الحسابات (التسجيل، الدخول، الخروج)
# ==========================================
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def make_admin_user(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', '12345678')
        return HttpResponse('<h2 dir="rtl" style="text-align:center; color:green;">تم إنشاء حساب المدير بنجاح!</h2>')
    return HttpResponse('<h2 dir="rtl" style="text-align:center; color:blue;">حساب المدير موجود مسبقاً.</h2>')

# ==========================================
# 2. نظام الإعلانات ولوحة التحكم
# ==========================================
def home(request):
    latest_ads = Ad.objects.filter(is_active=True)[:12]
    categories = Category.objects.all()
    return render(request, 'home.html', {'ads': latest_ads, 'categories': categories})

def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk, is_active=True)
    ad.views_count += 1
    ad.save(update_fields=['views_count'])
    return render(request, 'ad_detail.html', {'ad': ad})

@login_required(login_url='login')
def dashboard(request):
    user_ads = Ad.objects.filter(user=request.user)
    search_query = request.GET.get('search', '')
    
    if search_query:
        user_ads = user_ads.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    
    paginator = Paginator(user_ads, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'total_ads': user_ads.count(),
        'total_views': sum(ad.views_count for ad in user_ads),
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def add_ad(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        
        if title and description and price:
            category = Category.objects.filter(id=category_id).first() if category_id else None
            Ad.objects.create(user=request.user, category=category, title=title, description=description, price=price, image=image)
            messages.success(request, "تم نشر إعلانك بنجاح! 🚀")
            return redirect('dashboard')
            
    return render(request, 'add_ad.html', {'categories': categories})

@login_required(login_url='login')
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    if request.method == 'POST':
        ad.delete()
        messages.success(request, "تم الحذف بنجاح!")
        return redirect('dashboard')
    return render(request, 'confirm_delete.html', {'ad': ad})

from django.contrib.auth.models import User
from django.http import HttpResponse

def make_admin_view(path_request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', '12345678')
        return HttpResponse('تم إنشاء حساب المشرف بنجاح! اسم المستخدم: admin | كلمة المرور: 12345678. يمكنك تسجيل الدخول الآن.')
    return HttpResponse('حساب المشرف موجود مسبقاً بالفعل!')
