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
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ad, Category

@login_required
def add_ad(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        
        category = Category.objects.filter(id=category_id).first()
        
        Ad.objects.create(
            user=request.user,
            title=title,
            description=description,
            price=price,
            category=category,
            image=image
        )
        return redirect('dashboard')
        
    return render(request, 'add_ad.html', {'categories': categories})

def make_admin_view(path_request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', '12345678')
        return HttpResponse('تم إنشاء حساب المشرف بنجاح! اسم المستخدم: admin | كلمة المرور: 12345678. يمكنك تسجيل الدخول الآن.')
    return HttpResponse('حساب المشرف موجود مسبقاً بالفعل!')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Ad, Category

def home(request):
    latest_ads = Ad.objects.filter(is_active=True)[:6]
    categories = Category.objects.all()
    return render(request, 'home.html', {'ads': latest_ads, 'categories': categories})

@login_required
def dashboard(request):
    user_ads = Ad.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'ads': user_ads})

@login_required
def add_ad(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        
        category = Category.objects.filter(id=category_id).first()
        
        Ad.objects.create(
            user=request.user,
            title=title,
            description=description,
            price=price,
            category=category,
            image=image
        )
        return redirect('dashboard')
        
    return render(request, 'add_ad.html', {'categories': categories})

def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'ad_detail.html', {'ad': ad})

def make_admin_view(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', '12345678')
        return HttpResponse('تم إنشاء حساب المشرف بنجاح! اسم المستخدم: admin | كلمة المرور: 12345678. يمكنك تسجيل الدخول الآن.')
    return HttpResponse('حساب المشرف موجود مسبقاً بالفعل!')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.db.models import Q
from .models import Ad, Category

def home(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    
    ads = Ad.objects.filter(is_active=True).order_by('-created_at')
    
    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id:
        ads = ads.filter(category_id=category_id)
        
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'ads': ads,
        'categories': categories,
        'search_query': query,
        'selected_category': category_id
    })

def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    ad.views_count += 1
    ad.save(update_fields=['views_count'])
    return render(request, 'ad_detail.html', {'ad': ad})

@login_required
def dashboard(request):
    user_ads = Ad.objects.filter(user=request.user).order_by('-created_at')
    total_ads = user_ads.count()
    return render(request, 'dashboard.html', {
        'ads': user_ads,
        'total_ads': total_ads
    })

@login_required
def add_ad(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        
        category = Category.objects.filter(id=category_id).first()
        
        Ad.objects.create(
            user=request.user,
            title=title,
            description=description,
            price=price,
            category=category,
            image=image
        )
        return redirect('dashboard')
        
    return render(request, 'add_ad.html', {'categories': categories})

@login_required
def edit_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    categories = Category.objects.all()
    if request.method == 'POST':
        ad.title = request.POST.get('title')
        ad.description = request.POST.get('description')
        ad.price = request.POST.get('price')
        category_id = request.POST.get('category')
        ad.category = Category.objects.filter(id=category_id).first()
        if request.FILES.get('image'):
            ad.image = request.FILES.get('image')
        ad.save()
        return redirect('dashboard')
    return render(request, 'edit_ad.html', {'ad': ad, 'categories': categories})

@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    if request.method == 'POST':
        ad.delete()
        return redirect('dashboard')
    return render(request, 'delete_ad.html', {'ad': ad})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def make_admin_view(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', '12345678')
        return HttpResponse('تم إنشاء حساب المشرف بنجاح! اسم المستخدم: admin | كلمة المرور: 12345678.')
    return HttpResponse('حساب المشرف موجود مسبقاً بالفعل!')
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .models import Ad, Category

# --- دوال التصفح والبحث الذكي ---
def home(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    
    ads = Ad.objects.filter(is_active=True).order_by('-created_at')
    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id:
        ads = ads.filter(category_id=category_id)
        
    return render(request, 'home.html', {
        'ads': ads,
        'categories': Category.objects.all(),
        'search_query': query,
        'selected_category': category_id
    })

def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if hasattr(ad, 'views_count'):
        ad.views_count += 1
        ad.save(update_fields=['views_count'])
    return render(request, 'ad_detail.html', {'ad': ad})

# --- دوال لوحة التحكم وإدارة الإعلانات ---
@login_required
def dashboard(request):
    user_ads = Ad.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'ads': user_ads, 'total_ads': user_ads.count()})

@login_required
def add_ad(request):
    if request.method == 'POST':
        Ad.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            price=request.POST.get('price'),
            category=Category.objects.filter(id=request.POST.get('category')).first(),
            image=request.FILES.get('image')
        )
        return redirect('dashboard')
    return render(request, 'add_ad.html', {'categories': Category.objects.all()})

@login_required
def edit_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    if request.method == 'POST':
        ad.title = request.POST.get('title')
        ad.description = request.POST.get('description')
        ad.price = request.POST.get('price')
        ad.category = Category.objects.filter(id=request.POST.get('category')).first()
        if request.FILES.get('image'):
            ad.image = request.FILES.get('image')
        ad.save()
        return redirect('dashboard')
    return render(request, 'edit_ad.html', {'ad': ad, 'categories': Category.objects.all()})

@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk, user=request.user)
    if request.method == 'POST':
        ad.delete()
        return redirect('dashboard')
    return render(request, 'delete_ad.html', {'ad': ad})

# --- دوال الحسابات ---
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def make_admin_view(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', '12345678')
        return HttpResponse('تم إنشاء حساب المشرف بنجاح! اسم المستخدم: admin | كلمة المرور: 12345678.')
    return HttpResponse('حساب المشرف موجود مسبقاً بالفعل!')

# --- ميزة الذكاء الاصطناعي (AI Assistant) ---
def ai_generate_description(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title', '')
            if title:
                # محرك توليد ذكي مدمج (كخطوة أولى قبل ربطه بـ API خارجي لاحقاً)
                ai_text = f"🔥 فرصة مميزة! نقدم لكم '{title}' بحالة ممتازة ومواصفات رائعة. السعر منافس جداً وجاهز للتسليم الفوري. تواصل معنا الآن للمزيد من التفاصيل ولا تفوت هذه الفرصة!"
                return JsonResponse({'success': True, 'description': ai_text})
            return JsonResponse({'success': False, 'error': 'العنوان فارغ'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'طلب غير صالح'})
