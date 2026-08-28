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
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home')