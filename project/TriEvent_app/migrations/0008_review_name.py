# Generated by Django 3.2.9 on 2021-11-29 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TriEvent_app', '0007_auto_20211127_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='name',
            field=models.CharField(default='Anonim', max_length=120),
        ),
    ]
