# Generated by Django 5.2.2 on 2025-06-09 08:35

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('token', models.CharField(editable=False, max_length=128, unique=True)),
                ('doc_name', models.CharField(max_length=100)),
                ('sheet_name', models.CharField(max_length=100)),
                ('accounts', models.ManyToManyField(related_name='collections', to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='main.profile')),
            ],
        ),
        migrations.CreateModel(
            name='BD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.BigIntegerField()),
                ('album', models.TextField()),
                ('number', models.CharField(max_length=50)),
                ('series', models.TextField()),
                ('writer', models.TextField()),
                ('illustrator', models.TextField()),
                ('colorist', models.TextField()),
                ('publisher', models.TextField()),
                ('publication_date', models.DateField(null=True)),
                ('edition', models.TextField()),
                ('number_of_pages', models.IntegerField(null=True)),
                ('rating', models.FloatField(null=True)),
                ('purchase_price', models.FloatField(null=True)),
                ('year_of_purchase', models.IntegerField(null=True)),
                ('place_of_purchase', models.TextField()),
                ('deluxe_edition', models.BooleanField(default=False)),
                ('localisation', models.TextField()),
                ('synopsis', models.TextField()),
                ('image', models.URLField()),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rows', to='main.collection')),
            ],
        ),
        migrations.AddField(
            model_name='appuser',
            name='current_collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_users', to='main.collection'),
        ),
    ]
