# Generated by Django 4.2 on 2024-06-21 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Vacancie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vacancy_link', models.URLField(max_length=100)),
                ('vacancy_subcategory', models.CharField(blank=True, max_length=30, null=True)),
                ('vacancy_site', models.CharField(blank=True, max_length=10, null=True)),
                ('vacancy_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='courses.coursecategory')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=100)),
                ('course_workload', models.IntegerField()),
                ('teaching_plataform', models.CharField(blank=True, default='Desconhecido', max_length=100)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='courses/')),
                ('description', models.TextField(blank=True, null=True)),
                ('course_link', models.URLField(default='', max_length=100)),
                ('course_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='course_category', to='courses.coursecategory')),
            ],
        ),
    ]
