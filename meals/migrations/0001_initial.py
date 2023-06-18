# Generated by Django 4.2.2 on 2023-06-18 17:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('subtitle', models.TextField()),
                ('creator_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('measure_type', models.CharField(choices=[('100g', 'HundrGrams'), ('100ml', 'HundrMilis'), ('tsp', 'Teaspoon'), ('tbsp', 'Tablespoon'), ('glass', 'Glass')], max_length=10)),
                ('kcal', models.IntegerField()),
                ('isVerified', models.BooleanField()),
                ('creator_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MealElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('meal_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.meal')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.product')),
            ],
        ),
        migrations.AddField(
            model_name='meal',
            name='product_list',
            field=models.ManyToManyField(through='meals.MealElement', to='meals.product'),
        ),
    ]
