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
