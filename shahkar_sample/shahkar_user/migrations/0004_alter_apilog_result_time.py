# Generated by Django 4.2.16 on 2024-10-22 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shahkar_user', '0003_apilog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apilog',
            name='result_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
