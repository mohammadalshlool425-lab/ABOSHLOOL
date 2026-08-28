from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='اسم القسم')),
                ('icon', models.CharField(blank=True, help_text='كود أيقونة FontAwesome', max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان الإعلان')),
                ('description', models.TextField(verbose_name='التفاصيل')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='السعر')),
                ('image', models.ImageField(blank=True, null=True, upload_to='ads_images/', verbose_name='صورة الإعلان')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ النشر')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخر تحديث')),
                ('views_count', models.IntegerField(default=0, verbose_name='عدد المشاهدات')),
                ('is_active', models.BooleanField(default=True, verbose_name='متاح؟')),
                ('category', models.ForeignKey(null=True, on_delete=models.deletion.SET_NULL, to='core.category', verbose_name='القسم')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='ads', to=settings.AUTH_USER_MODEL, verbose_name='المعلن')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
