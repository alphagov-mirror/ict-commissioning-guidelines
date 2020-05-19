# Generated by Django 3.0.5 on 2020-05-19 14:25

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0002_auto_20200423_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moreinformationmodule',
            name='link_text',
        ),
        migrations.RemoveField(
            model_name='moreinformationmodule',
            name='open_in_new_tab',
        ),
        migrations.RemoveField(
            model_name='moreinformationmodule',
            name='url',
        ),
        migrations.AlterField(
            model_name='moreinformationmodule',
            name='description',
            field=wagtail.core.fields.RichTextField(blank=True, default=''),
        ),
    ]
