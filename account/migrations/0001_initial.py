# Generated by Django 4.0.3 on 2022-04-08 00:00

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$'), 'Informe um nome de usuário válido. Este valor deve conter apenas letras, números e os caracteres: @/./+/-/_ .', 'invalid')], verbose_name='Usuário')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Nome Completo')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Equipe')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'Administrativo'), (4, 'Curador'), (5, 'Cliente')], default=1, verbose_name='Tipo usuário')),
                ('user_picture', models.ImageField(blank=True, null=True, upload_to='users_pictures', verbose_name='Imagem')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Data de Registro')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
