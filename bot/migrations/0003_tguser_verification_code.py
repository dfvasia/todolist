# Generated by Django 4.0.5 on 2022-07-09 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_alter_tguser_chat_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tguser',
            name='verification_code',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
