from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ad(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='ads/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
        from django.db import models
from django.contrib.auth.models import User

# جدول الأقسام (سيارات، عقارات، إلكترونيات...)
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="اسم القسم")
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="كود أيقونة FontAwesome")

    def __str__(self):
        return self.name

# جدول الإعلانات الرئيسي
class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads', verbose_name="المعلن")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="القسم")
    title = models.CharField(max_length=200, verbose_name="عنوان الإعلان")
    description = models.TextField(verbose_name="التفاصيل")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="السعر")
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True, verbose_name="صورة الإعلان")
    
    # حقول ذكية للتتبع
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ النشر")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")
    views_count = models.IntegerField(default=0, verbose_name="عدد المشاهدات")
    is_active = models.BooleanField(default=True, verbose_name="متاح؟")

    class Meta:
        ordering = ['-created_at'] # الترتيب الافتراضي من الأحدث للأقدم

    def __str__(self):
        return f"{self.title} - {self.price} JOD"
