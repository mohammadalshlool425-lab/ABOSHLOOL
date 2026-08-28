from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Ad, Category

def home(request):
    query = request.GET.get('q', '')
    ads = Ad.objects.all().order_by('-created_at')
    
    if query:
        ads = ads.filter(title__icontains=query) | ads.filter(description__icontains=query)
        
    return render(request, 'home.html', {'ads': ads, 'query': query})

@login_required(login_url='login')
def add_ad(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        
        category = Category.objects.filter(id=category_id).first() if category_id else None
        
        Ad.objects.create(
            title=title,
            description=description,
            price=price,
            category=category,
            image=image,
            user=request.user
        )
        return redirect('dashboard')
        
    return render(request, 'add_ad.html', {'categories': categories})

def ad_detail(request, pk):
    ad = Ad.objects.filter(id=pk).first()
    if not ad:
        return redirect('home')
    return render(request, 'ad_detail.html', {'ad': ad})

@login_required(login_url='login')
def dashboard_view(request):
    user_ads = Ad.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'ads': user_ads})

@login_required(login_url='login')
def delete_ad(request, pk):
    ad = Ad.objects.filter(id=pk, user=request.user).first()
    if ad:
        ad.delete()
    return redirect('dashboard')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        from django.contrib.auth.models import User
from django.http import HttpResponse

def make_admin_user(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', '12345678')
        return HttpResponse('<h2 dir="rtl" style="text-align:center; margin-top:50px; color:green;">تم بنجاح! الرابط الجديد اشتغل وتم إنشاء المدير.</h2>')
    return HttpResponse('<h2 dir="rtl" style="text-align:center; margin-top:50px; color:blue;">حساب المدير موجود مسبقاً، يمكنك تسجيل الدخول الآن.</h2>')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home')
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import Ad  # تأكد إن اسم الكلاس تبع الإعلانات هو Ad في ملف models.py

@login_required(login_url='login')
def dashboard(request):
    """
    لوحة تحكم احترافية للمستخدم: تشمل إحصائيات، بحث متطور، فلترة، وتقسيم صفحات.
    """
    # 1. جلب المستخدم الحالي
    user = request.user

    # 2. استدعاء إعلانات المستخدم فقط (مستحيل يشوف إعلانات غيره)
    user_ads = Ad.objects.filter(user=user)
    
    # 3. الإحصائيات (لمحاكاة لوحات تحكم المتاجر الكبرى)
    total_ads_count = user_ads.count()

    # 4. محرك بحث ذكي داخل لوحة التحكم (يبحث في العنوان والتفاصيل معاً)
    search_query = request.GET.get('search', '')
    if search_query:
        user_ads = user_ads.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    # 5. نظام الفلترة والترتيب (مهم جداً إذا بتعرض قطع كمبيوتر أو سيارات)
    # الترتيب الافتراضي هو الأحدث
    sort_by = request.GET.get('sort', '-created_at') 
    valid_sorts = ['price', '-price', 'created_at', '-created_at']
    if sort_by in valid_sorts:
        user_ads = user_ads.order_by(sort_by)

    # 6. نظام تقسيم الصفحات (Pagination) عشان الموقع يضل "طلقة"
    # يعرض 10 إعلانات فقط في كل صفحة لتوفير موارد السيرفر
    paginator = Paginator(user_ads, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 7. تغليف البيانات وإرسالها للواجهة الأمامية
    context = {
        'user': user,
        'total_ads_count': total_ads_count,
        'page_obj': page_obj,
        'search_query': search_query,
        'sort_by': sort_by,
    }

    # 8. عرض قالب الـ HTML (الواجهة)
    return render(request, 'core/dashboard.html', context)
