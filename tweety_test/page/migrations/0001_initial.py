# Generated by Django 5.0.4 on 2024-06-02 18:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connect', models.BooleanField(default=False)),
                ('name', models.CharField(default='None', max_length=20)),
                ('platform', models.CharField(max_length=20)),
                ('email', models.CharField(default='None', max_length=20)),
                ('password', models.CharField(default='None', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tag', models.CharField(default='None', max_length=20)),
                ('color', models.CharField(default='None', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='None', max_length=20)),
                ('platform', models.CharField(max_length=20, null=True)),
                ('text', models.TextField()),
                ('images', models.JSONField()),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('tag', models.CharField(default='None', max_length=20)),
                ('Account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='page.account')),
            ],
        ),
    ]