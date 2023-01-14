# Generated by Django 3.1 on 2023-01-13 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("dashboard", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("blogIdea", models.CharField(max_length=100)),
                ("title", models.CharField(max_length=100)),
                ("audience", models.CharField(blank=True, max_length=100, null=True)),
                ("keywords", models.CharField(blank=True, max_length=100, null=True)),
                ("word_count", models.CharField(blank=True, max_length=100, null=True)),
                ("uniqueId", models.CharField(blank=True, max_length=100, null=True)),
                ("slug", models.SlugField(blank=True, max_length=500, null=True, unique=True)),
                ("dateCreated", models.DateTimeField(blank=True, null=True)),
                ("lastUpdated", models.DateTimeField(blank=True, null=True)),
                ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="dashboard.profile")),
            ],
        ),
        migrations.CreateModel(
            name="BlogSection",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100)),
                ("body", models.TextField(blank=True, null=True)),
                ("word_count", models.CharField(blank=True, max_length=100, null=True)),
                ("uniqueId", models.CharField(blank=True, max_length=100, null=True)),
                ("slug", models.SlugField(blank=True, max_length=500, null=True, unique=True)),
                ("dateCreated", models.DateTimeField(blank=True, null=True)),
                ("lastUpdated", models.DateTimeField(blank=True, null=True)),
                ("blog", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="blog.blog")),
            ],
        ),
    ]
