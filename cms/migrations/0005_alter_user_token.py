# Generated by Django 3.2.25 on 2025-01-12 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_alter_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, default='129a55e2-284c-4088-875a-ec3fb819caa4', max_length=500, null=True),
        ),
    ]
