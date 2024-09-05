# Generated by Django 5.1.1 on 2024-09-05 06:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


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
                ('title', models.CharField(max_length=32)),
                ('description', models.TextField(max_length=250)),
                ('y_display', models.SmallIntegerField(default=-1)),
                ('staff_only', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['-y_display'],
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('description', models.TextField(max_length=250)),
                ('y_display', models.SmallIntegerField(default=-1)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.category')),
            ],
            options={
                'verbose_name_plural': 'subcategories',
                'ordering': ['-y_display'],
            },
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('pinned', models.BooleanField(default=False)),
                ('locked', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.subcategory')),
            ],
            options={
                'ordering': ['-pk'],
                'permissions': [('locked_thread_reply', 'Can reply to a locked thread.'), ('create_thread_in_staff_only', 'Can create threads in staff only categories.')],
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=25000)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('downvoters', models.ManyToManyField(blank=True, related_name='upvoters', to=settings.AUTH_USER_MODEL)),
                ('upvoters', models.ManyToManyField(blank=True, related_name='downvoters', to=settings.AUTH_USER_MODEL)),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.thread')),
            ],
        ),
    ]
