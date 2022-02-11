from django.db import models
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import warnings
warnings.filterwarnings('ignore')

import io
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

# Create your models here.


class AddProgramAndFacultyName(models.Model):
    program_name_by_hr = models.CharField(max_length=1000,blank=False)
    faculty_name_by_hr = models.CharField(max_length=1000,blank=False)
    location_of_training = models.CharField(max_length=1000,blank=False)
    Date_of_Training = models.CharField(max_length=1000,blank=False)

    def __str__(self):
        return self.program_name_by_hr + ' By ' + self.faculty_name_by_hr + ' on ' + self.Date_of_Training + ' --- ID is - ' + str(self.id)


class FeedbackDetail(models.Model):
    Program_Name = models.CharField(max_length=255, blank=False)
    Faculty_Name = models.CharField(max_length=255, blank=False)
    Date_of_Training = models.CharField(max_length=255, blank=False)
    location = models.CharField(max_length=255, blank=False)
    country = models.CharField(max_length=255, blank=False)
    sap_id = models.CharField(max_length=7, blank=False, verbose_name = "Company ID 7 digits")
    email_id = models.CharField(max_length=255, blank=False)
    how_would_you_rate_the_program = models.CharField(max_length=1, choices=[('5','Excellent'),('4','Very Good'),('3','Good'),('2','Bad'),('1','Very Bad')], blank=False, default='Unspecified')
    additional_comments_for_program = models.CharField(max_length=255, blank=True, verbose_name = "Additional comments for traning (If any):")
    how_would_you_rate_the_faculty_delivery = models.CharField(max_length=1, verbose_name = "How would you rate the faculty delivery:", choices=[('5','Excellent'),('4','Very Good'),('3','Good'),('2','Bad'),('1','Very Bad')], blank=False, default='Unspecified')
    additional_comments_for_faculty = models.CharField(max_length=255, blank=True, verbose_name = "Additional comments for faculty (If any):")

    def __str__(self):
        return str(self.Program_Name) + ' By - ' + str(self.Faculty_Name) + ' on date - ' + str(self.Date_of_Training)


class SendEmailToTrainer(models.Model):
    Select_Faculty_Name = models.ForeignKey(AddProgramAndFacultyName, default=1, on_delete=models.SET_DEFAULT)
    Mode_of_Training = models.CharField(max_length=255, choices=[('Classroom', 'Classroom'), ('Virtual', 'Virtual'), ('Classroom/Virtual', 'Classroom/Virtual')],blank=False)
    Faculty_Diversity = models.CharField(max_length=255, choices=[('Male', 'Male'), ('Female', 'Female'),
                                                                  ('Co Facilitation', 'Co Facilitation')], blank=False)
    from_person = models.EmailField(max_length=1000, blank=False)
    from_app_password = models.CharField(max_length=1000, blank=False)
    Trainer_email_address = models.CharField(max_length=1000, blank=False, verbose_name = "Trainer's email address")
    Other_email_address_in_CC = models.CharField(max_length=1000, verbose_name = "Other email address in CC")
    send_it = models.BooleanField(default=False)  # check it if you want to send your email

    def save(self):
        count = 0
        if self.send_it and count <= 0:
            count += 1
            # First you create your list of users
            df_user = pd.DataFrame(list(FeedbackDetail.objects.all().values()))
            df_user['choice_for_hr'] = df_user['Program_Name'] + ' By ' + df_user['Faculty_Name'] + ' on ' + df_user['Date_of_Training']
            df_hr = pd.DataFrame(list(AddProgramAndFacultyName.objects.all().values()))
            df_hr['choice_for_hr'] = df_hr['program_name_by_hr'] + ' By ' + df_hr['faculty_name_by_hr'] + ' on ' + df_hr['Date_of_Training']
            df_merge = pd.merge(df_user, df_hr, on=['choice_for_hr','Date_of_Training'], how='outer')
            df_all = df_merge.dropna(subset=['id_y'])
            df_all = df_all.loc[df_all['choice_for_hr'] == (str(self.Select_Faculty_Name).split('---')[0].strip())]
            df_all = df_all.reset_index(drop=True)

            def find_rating(col, df_single_trainee):
                denominator = len(df_single_trainee)*5
                df_trainee_rating = df_single_trainee[col].value_counts().reset_index()
                df_trainee_rating['rating'] = df_trainee_rating['index'].apply(lambda x: int(x[-1]))
                df_trainee_rating['total_rating'] = df_trainee_rating[col]*df_trainee_rating['rating']
                numerator = sum(df_trainee_rating['total_rating'])
                rating_percentage = round((numerator/denominator)*100)
                return rating_percentage

            program_name = df_all['Program_Name'][0]
            classroom_virtual = str(self.Mode_of_Training)
            program_dates = df_all['Date_of_Training'][0]
            location = df_all['location'][0]
            faculty_diversity = str(self.Faculty_Diversity)
            faculty_name = df_all['Faculty_Name'][0]
            final_program_rating = find_rating('how_would_you_rate_the_program', df_all)
            final_trainee_rating = find_rating('how_would_you_rate_the_faculty_delivery', df_all)

            ####################### email
            # from your account
            fromaddr = str(self.from_person)
            to_email_list = self.Trainer_email_address
            toaddr = to_email_list.split(',')
            cc_email_list = self.Other_email_address_in_CC
            ccaddr = cc_email_list.split(',')

            # instance of MIMEMultipart
            doc_msg = MIMEMultipart()
            # storing the senders email address
            doc_msg['From'] = fromaddr
            # storing the receivers email address
            doc_msg['To'] = ','.join(toaddr)
            # storing the Cc email address
            doc_msg['Cc'] = ','.join(ccaddr)

            doc_msg['Subject'] = 'Thank You || Feedback Scores || {0} || {1}'.format(program_name, program_dates)
            body = '''
            <html>
            Hi,<br/><br/> We would like to share your feedback scores for facilitating <b>{0}</b> on <b>{1}.</b> <br/><br/>
			<br/><br/> <b> Thank you for facilitating this session  :) </b> <br/><br/>
            <table style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">
                <tr style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;"><th colspan='2'>Training Feedback Report</th></tr>
              <tr style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;"><b>Training Program Name</b></td>
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">{2}</td>
              </tr>
              <tr style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;"><b>Classroom / Virtual</b></td>
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">{3}</td>
              </tr>
              <tr style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;"><b>No. of Participants who gave feedback</b></td>
                <td>{4}</td>
              </tr>
              <tr style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;"><b>Program Dates</b></td>
                <td>{5}</td>
              </tr>
              <tr style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;"><b>Location</b></td>
                <td>{6}</td>
              </tr>
              <tr style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;"><b>Faculty Diversity (Male / Female / Co Facilitation)</b></td>
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">{7}</td>
              </tr>
              <tr style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;"><b>Faculty(ies') Name(s)</b></td>
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">{8}</td>
              </tr>
              <tr style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;"><b>Facilitator Rating (on a 5 point rating Scale)</b></td>
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">{9}%</td>
              </tr>
               <tr style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;"><b>Program Rating (on a 5 Point rating Scale)</b></td>
                <td style=" text-align:center; padding: 5px; border-collapse: collapse; border: 1px solid black;">{10}%</td>
              </tr>
            </table><br/></br> Please click on the Feedback file to review participant comments. </br></br>
            </html>'''.format(program_name, program_dates, program_name, classroom_virtual, len(df_all), program_dates,
            location, faculty_diversity, faculty_name, final_program_rating, final_trainee_rating)

            doc_msg.attach(MIMEText(body, 'html'))

            # open the file to be sent
            def export_csv(df_merge):
                with io.StringIO() as buffer:
                    df_merge.to_csv(buffer)
                    return buffer.getvalue()

            df_all = df_all[['Program_Name','Faculty_Name','Date_of_Training','location','country','how_would_you_rate_the_program','how_would_you_rate_the_faculty_delivery','additional_comments_for_faculty']]
            EXPORTERS = {'{0} on {1}.csv'.format(program_name, program_dates): export_csv}
            for filename in EXPORTERS:
                attachment = MIMEApplication(EXPORTERS[filename](df_all))
                attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                doc_msg.attach(attachment)
            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
            # start TLS for security
            s.starttls()
            # Authentication
            s.login(fromaddr, str(self.from_app_password))
            # Converts the Multipart msg into a string
            doc_text = doc_msg.as_string()
            # sending the doc mail
            s.sendmail(fromaddr, toaddr + ccaddr, doc_text)
            # terminating the session
            s.quit()

    def __str__(self):
        return 'Send email to trainers - ' + str(self.Select_Faculty_Name) + ' Email sent by - ' + str(self.from_person)


class ExportTrainingFeedbackScore(models.Model):
    Select_Faculty_Name = models.ForeignKey(AddProgramAndFacultyName, default=1, on_delete=models.SET_DEFAULT)
    from_person = models.EmailField(max_length=1000, blank=False)
    from_app_password = models.CharField(max_length=1000, blank=False)
    Trainer_email_address = models.CharField(max_length=1000, blank=False, verbose_name = "Trainer's email address")
    Other_email_address_in_CC = models.CharField(max_length=1000, blank=True, verbose_name = "Other email address in CC")
    send_it = models.BooleanField(default=False)  # check it if you want to send your email

    def save(self):
        if self.send_it:
            df_merge = pd.DataFrame(list(FeedbackDetail.objects.all().values()))
            df_merge['choice_for_hr'] = df_merge['Program_Name'] + ' By ' + df_merge['Faculty_Name'] + ' on ' + df_merge['Date_of_Training']
            df_merge = df_merge.loc[df_merge['choice_for_hr'] == (str(self.Select_Faculty_Name).split('---')[0].strip())]

            fromaddr = str(self.from_person)
            to_email_list = self.Trainer_email_address
            doc_toaddr = to_email_list.split(',')
            cc_email_list = self.Other_email_address_in_CC
            doc_ccaddr = cc_email_list.split(',')

            # instance of MIMEMultipart
            doc_msg = MIMEMultipart()
            # storing the senders email address
            doc_msg['From'] = fromaddr
            # storing the receivers email address
            doc_msg['To'] = ','.join(doc_toaddr)
            # storing the Cc email address
            doc_msg['Cc'] = ','.join(doc_ccaddr)
            # storing the subject
            doc_msg['Subject'] = "Details from Database for - {}".format(str(self.Select_Faculty_Name))
            doc_body = '''<html>
            Hi,<br/><br/> Please find feedback data from Database <br/><br/> Thanks.<br/></html>'''
            # attach the body with the msg instance
            doc_msg.attach(MIMEText(doc_body, 'html'))

            # open the file to be sent
            def export_csv(df_merge):
                with io.StringIO() as buffer:
                    df_merge.to_csv(buffer)
                    return buffer.getvalue()

            EXPORTERS = {'datafromdatabase.csv': export_csv}
            for filename in EXPORTERS:
                attachment = MIMEApplication(EXPORTERS[filename](df_merge))
                attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                doc_msg.attach(attachment)
            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
            # start TLS for security
            s.starttls()
            # Authentication
            s.login(fromaddr, str(self.from_app_password))
            # Converts the Multipart msg into a string
            doc_text = doc_msg.as_string()
            # sending the doc mail
            s.sendmail(fromaddr, doc_toaddr + doc_ccaddr, doc_text)
            # terminating the session
            s.quit()

    def __str__(self):
        return 'Export training feedback scores - ' + str(self.Select_Faculty_Name) + ' Email sent by - ' + str(self.from_person)


class SendReminder(models.Model):
    Select_Faculty_Name = models.ForeignKey(AddProgramAndFacultyName, default=1, on_delete=models.SET_DEFAULT)
    from_person = models.EmailField(max_length=1000, blank=False)
    from_app_password = models.CharField(max_length=1000, blank=False)
    Trainer_email_address = models.CharField(max_length=1000, blank=False, verbose_name="Trainer's email address")
    Other_email_address_in_CC = models.CharField(max_length=1000,blank=True, verbose_name="Other email address in CC")
    send_it = models.BooleanField(default=False)  # check it if you want to send your email

    def save(self):
        if self.send_it:
            fromaddr = str(self.from_person)
            to_email_list = self.Trainer_email_address
            doc_toaddr = to_email_list.split(',')
            cc_email_list = self.Other_email_address_in_CC
            doc_ccaddr = cc_email_list.split(',')

            # instance of MIMEMultipart
            doc_msg = MIMEMultipart()
            # storing the senders email address
            doc_msg['From'] = fromaddr
            # storing the receivers email address
            doc_msg['To'] = ','.join(doc_toaddr)
            # storing the Cc email address
            doc_msg['Cc'] = ','.join(doc_ccaddr)

            # storing the subject
            doc_msg['Subject'] = "Reminder : Feedback for - {} ".format(str(self.Select_Faculty_Name).split('---')[0].strip())
            doc_body = """<html>
            Dear All,<br/><br/> Please consider this mail as a reminder for obtaining your feedback for """+str(self.Select_Faculty_Name).split('---')[0].strip()+""".<br/><br/> 
            Request you to please provide your feedback by clicking on the below link:- <br/><br/> 
            http://3.7.44.215/feedbackdetails/"""+str(self.Select_Faculty_Name).split('--- ID is - ')[1].strip()+"""<br/><br/> 
            Please ignore if feedback already provided.<br/><br/>
            Thank you<br/><br/>
            TED Team.
            </html>"""

            # attach the body with the msg instance
            doc_msg.attach(MIMEText(doc_body, 'html'))
            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
            # start TLS for security
            s.starttls()
            # Authentication
            s.login(fromaddr, str(self.from_app_password))
            # Converts the Multipart msg into a string
            doc_text = doc_msg.as_string()
            # sending the doc mail
            s.sendmail(fromaddr, doc_toaddr + doc_ccaddr, doc_text)
            # terminating the session
            s.quit()

    def __str__(self):
        return 'Send reminders - ' + str(self.Select_Faculty_Name) + ' Email sent by - ' + str(self.from_person)

class ExportTableOnSapId(models.Model):
    Enter_SAP_ID = models.CharField(max_length=7, blank=False)
    from_person = models.EmailField(max_length=1000, blank=False)
    from_app_password = models.CharField(max_length=1000, blank=False)
    Trainer_email_address = models.CharField(max_length=1000, blank=False, verbose_name = "Trainer's email address")
    Other_email_address_in_CC = models.CharField(max_length=1000, blank=True, verbose_name = "Other email address in CC")
    send_it = models.BooleanField(default=False)  # check it if you want to send your email

    def save(self):
        if self.send_it:
            df_merge = pd.DataFrame(list(FeedbackDetail.objects.all().values()))
            df_merge = df_merge.loc[df_merge['sap_id'] == self.Enter_SAP_ID]

            fromaddr = str(self.from_person)
            to_email_list = self.Trainer_email_address
            doc_toaddr = to_email_list.split(',')
            cc_email_list = self.Other_email_address_in_CC
            doc_ccaddr = cc_email_list.split(',')

            # instance of MIMEMultipart
            doc_msg = MIMEMultipart()
            # storing the senders email address
            doc_msg['From'] = fromaddr
            # storing the receivers email address
            doc_msg['To'] = ','.join(doc_toaddr)
            # storing the Cc email address
            doc_msg['Cc'] = ','.join(doc_ccaddr)
            # storing the subject
            doc_msg['Subject'] = "Details from Database for SAP ID:- {}".format(str(self.Enter_SAP_ID))
            doc_body = '''<html>
            Hi,<br/><br/> Please find data based on SAP ID from Database. <br/><br/> Thanks.<br/></html>'''
            # attach the body with the msg instance
            doc_msg.attach(MIMEText(doc_body, 'html'))

            # open the file to be sent
            def export_csv(df_merge):
                with io.StringIO() as buffer:
                    df_merge.to_csv(buffer)
                    return buffer.getvalue()

            EXPORTERS = {'sap_id_database.csv': export_csv}
            for filename in EXPORTERS:
                attachment = MIMEApplication(EXPORTERS[filename](df_merge))
                attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                doc_msg.attach(attachment)
            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
            # start TLS for security
            s.starttls()
            # Authentication
            s.login(fromaddr, str(self.from_app_password))
            # Converts the Multipart msg into a string
            doc_text = doc_msg.as_string()
            # sending the doc mail
            s.sendmail(fromaddr, doc_toaddr + doc_ccaddr, doc_text)
            # terminating the session
            s.quit()

    def __str__(self):
        return 'Export data for SAP ID  - ' + str(self.Enter_SAP_ID) + ' Email sent by - ' + str(self.from_person)

class ExportAllDatabase(models.Model):
    from_person = models.EmailField(max_length=1000, blank=False)
    from_app_password = models.CharField(max_length=1000, blank=False)
    Trainer_email_address = models.CharField(max_length=1000, blank=False, verbose_name = "Trainer's email address")
    Other_email_address_in_CC = models.CharField(max_length=1000, blank=True, verbose_name = "Other email address in CC")
    send_it = models.BooleanField(default=False)  # check it if you want to send your email

    def save(self):
        if self.send_it:
            df_merge = pd.DataFrame(list(FeedbackDetail.objects.all().values()))
            df_merge = df_merge[['id','Program_Name','Faculty_Name','Date_of_Training','location','country','sap_id','email_id',
                                 'how_would_you_rate_the_program','how_would_you_rate_the_faculty_delivery','additional_comments_for_faculty']]
            fromaddr = str(self.from_person)
            to_email_list = self.Trainer_email_address
            doc_toaddr = to_email_list.split(',')
            cc_email_list = self.Other_email_address_in_CC
            doc_ccaddr = cc_email_list.split(',')

            # instance of MIMEMultipart
            doc_msg = MIMEMultipart()
            # storing the senders email address
            doc_msg['From'] = fromaddr
            # storing the receivers email address
            doc_msg['To'] = ','.join(doc_toaddr)
            # storing the Cc email address
            doc_msg['Cc'] = ','.join(doc_ccaddr)
            # storing the subject
            doc_msg['Subject'] = "Entire Database form django website"
            doc_body = '''<html>
            Hi,<br/><br/> Please find data from Database. <br/><br/> Thanks.<br/></html>'''
            # attach the body with the msg instance
            doc_msg.attach(MIMEText(doc_body, 'html'))

            # open the file to be sent
            def export_csv(df_merge):
                with io.StringIO() as buffer:
                    df_merge.to_csv(buffer)
                    return buffer.getvalue()

            EXPORTERS = {'database.csv': export_csv}
            for filename in EXPORTERS:
                attachment = MIMEApplication(EXPORTERS[filename](df_merge))
                attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
                doc_msg.attach(attachment)
            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
            # start TLS for security
            s.starttls()
            # Authentication
            s.login(fromaddr, str(self.from_app_password))
            # Converts the Multipart msg into a string
            doc_text = doc_msg.as_string()
            # sending the doc mail
            s.sendmail(fromaddr, doc_toaddr + doc_ccaddr, doc_text)
            # terminating the session
            s.quit()

    def __str__(self):
        return 'Export data form database  - Email sent by - ' + str(self.from_person)