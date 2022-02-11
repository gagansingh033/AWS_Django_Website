# Generated by Django 2.0.7 on 2020-06-09 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddProgramAndFacultyName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_name_by_hr', models.CharField(max_length=1000)),
                ('faculty_name_by_hr', models.CharField(max_length=1000)),
                ('location_of_training', models.CharField(max_length=1000)),
                ('Date_of_Training', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='ExportAllDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_person', models.EmailField(max_length=1000)),
                ('from_app_password', models.CharField(max_length=1000)),
                ('Trainer_email_address', models.CharField(max_length=1000, verbose_name="Trainer's email address")),
                ('Other_email_address_in_CC', models.CharField(blank=True, max_length=1000, verbose_name='Other email address in CC')),
                ('send_it', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExportTableOnSapId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Enter_SAP_ID', models.CharField(max_length=7)),
                ('from_person', models.EmailField(max_length=1000)),
                ('from_app_password', models.CharField(max_length=1000)),
                ('Trainer_email_address', models.CharField(max_length=1000, verbose_name="Trainer's email address")),
                ('Other_email_address_in_CC', models.CharField(blank=True, max_length=1000, verbose_name='Other email address in CC')),
                ('send_it', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExportTrainingFeedbackScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_person', models.EmailField(max_length=1000)),
                ('from_app_password', models.CharField(max_length=1000)),
                ('Trainer_email_address', models.CharField(max_length=1000, verbose_name="Trainer's email address")),
                ('Other_email_address_in_CC', models.CharField(blank=True, max_length=1000, verbose_name='Other email address in CC')),
                ('send_it', models.BooleanField(default=False)),
                ('Select_Faculty_Name', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='feedbackapp.AddProgramAndFacultyName')),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Program_Name', models.CharField(max_length=255)),
                ('Faculty_Name', models.CharField(max_length=255)),
                ('Date_of_Training', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('sap_id', models.CharField(max_length=7)),
                ('email_id', models.CharField(max_length=255)),
                ('how_would_you_rate_the_program', models.CharField(choices=[('5', 'Excellent'), ('4', 'Very Good'), ('3', 'Good'), ('2', 'Bad'), ('1', 'Very Bad')], default='Unspecified', max_length=1)),
                ('how_would_you_rate_the_faculty_delivery', models.CharField(choices=[('5', 'Excellent'), ('4', 'Very Good'), ('3', 'Good'), ('2', 'Bad'), ('1', 'Very Bad')], default='Unspecified', max_length=1, verbose_name='How would you rate the faculty delivery:')),
                ('additional_comments', models.CharField(blank=True, max_length=255, verbose_name='Additional comments (If any):')),
            ],
        ),
        migrations.CreateModel(
            name='SendEmailToTrainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Mode_of_Training', models.CharField(choices=[('Classroom', 'Classroom'), ('Virtual', 'Virtual'), ('Classroom/Virtual', 'Classroom/Virtual')], max_length=255)),
                ('Faculty_Diversity', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Co Facilitation', 'Co Facilitation')], max_length=255)),
                ('from_person', models.EmailField(max_length=1000)),
                ('from_app_password', models.CharField(max_length=1000)),
                ('Trainer_email_address', models.CharField(max_length=1000, verbose_name="Trainer's email address")),
                ('Other_email_address_in_CC', models.CharField(max_length=1000, verbose_name='Other email address in CC')),
                ('send_it', models.BooleanField(default=False)),
                ('Select_Faculty_Name', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='feedbackapp.AddProgramAndFacultyName')),
            ],
        ),
        migrations.CreateModel(
            name='SendReminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_person', models.EmailField(max_length=1000)),
                ('from_app_password', models.CharField(max_length=1000)),
                ('Trainer_email_address', models.CharField(max_length=1000, verbose_name="Trainer's email address")),
                ('Other_email_address_in_CC', models.CharField(blank=True, max_length=1000, verbose_name='Other email address in CC')),
                ('send_it', models.BooleanField(default=False)),
                ('Select_Faculty_Name', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='feedbackapp.AddProgramAndFacultyName')),
            ],
        ),
    ]