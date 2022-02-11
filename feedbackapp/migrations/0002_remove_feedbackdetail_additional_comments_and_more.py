# Generated by Django 4.0.1 on 2022-01-23 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedbackapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackdetail',
            name='additional_comments',
        ),
        migrations.AddField(
            model_name='feedbackdetail',
            name='additional_comments_for_faculty',
            field=models.CharField(blank=True, max_length=255, verbose_name='Additional comments for faculty (If any):'),
        ),
        migrations.AddField(
            model_name='feedbackdetail',
            name='additional_comments_for_program',
            field=models.CharField(blank=True, max_length=255, verbose_name='Additional comments for traning (If any):'),
        ),
        migrations.AlterField(
            model_name='feedbackdetail',
            name='sap_id',
            field=models.CharField(max_length=7, verbose_name='Company ID 7 digits'),
        ),
    ]