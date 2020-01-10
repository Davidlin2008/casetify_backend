# Generated by Django 3.0.1 on 2020-01-10 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('mobile_number', models.CharField(max_length=11, unique=True)),
                ('nick_name', models.CharField(max_length=100)),
                ('introduction', models.CharField(max_length=500, null=True)),
                ('website', models.URLField(max_length=2500, null=True)),
                ('location', models.CharField(max_length=500, null=True)),
                ('twitter', models.CharField(max_length=200, null=True)),
                ('image', models.URLField(max_length=2500, null=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=500, null=True)),
                ('zipcode', models.CharField(max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
