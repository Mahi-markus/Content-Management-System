# Generated by Django 3.2.25 on 2025-01-10 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, default='b081f7b9-6e41-4800-a0a2-cf414409b6c0', max_length=500, null=True),
        ),
    ]
