# Generated by Django 3.0.5 on 2020-06-12 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guidelines', '0006_auto_20200608_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guidelinessectionpage',
            name='section_colour',
            field=models.CharField(choices=[('primary-1', 'Primary 1'), ('primary-2', 'Primary 2'), ('primary-3', 'Primary 3'), ('primary-4', 'Primary 4')], max_length=140),
        ),
    ]
