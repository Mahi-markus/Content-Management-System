# Generated by Django 3.2.25 on 2025-01-13 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_alter_user_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, default='167f8957-0257-42f3-ad17-ab8c511e8ce6', max_length=500, null=True),
        ),
    ]
