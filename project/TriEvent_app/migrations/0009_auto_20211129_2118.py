# Generated by Django 3.2.9 on 2021-11-29 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TriEvent_app', '0008_review_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athlete',
            name='age_group',
            field=models.CharField(choices=[('UNDER-19', 'UNDER-19'), ('20-24', '20-24'), ('25-29', '25-29'), ('30-34', '30-34'), ('35-39', '35-39'), ('40-44', '40-44'), ('45-49', '45-49'), ('50-54', '50-54'), ('55-59', '55-59'), ('60-64', '60-64'), ('65-OVER', '65-OVER')], max_length=15),
        ),
        migrations.AlterField(
            model_name='athlete',
            name='proficiency',
            field=models.CharField(choices=[('amateur', 'amateur'), ('professional', 'professional')], default=None, max_length=30),
        ),
    ]
