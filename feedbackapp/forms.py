from django.forms import ModelForm
from feedbackapp.models import FeedbackDetail
from django import forms

class UserModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)
        self.fields['how_would_you_rate_the_faculty_delivery'].strip = False


    class Meta:
        model = FeedbackDetail
        fields = ['Program_Name', 'Faculty_Name', 'Date_of_Training','location','country', 'sap_id', 'email_id',
                  'how_would_you_rate_the_program','additional_comments_for_program',
                  'how_would_you_rate_the_faculty_delivery','additional_comments_for_faculty']
        widgets = {'Program_Name':forms.TextInput(),
                    'Faculty_Name':forms.TextInput(),
                    'Date_of_Training':forms.TextInput(),
                    'location':forms.TextInput(),
                   'country':forms.TextInput(),
                   'sap_id':forms.TextInput(),
                   'email_id':forms.TextInput(),
                   'how_would_you_rate_the_program':forms.RadioSelect(),
                   'additional_comments_for_program':forms.TextInput(),
                   'how_would_you_rate_the_faculty_delivery':forms.RadioSelect(),
                   'additional_comments_for_faculty':forms.TextInput()}
