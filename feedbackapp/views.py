from django.shortcuts import render
from django.db import models
from feedbackapp.models import AddProgramAndFacultyName
# Create your views here.

from .forms import UserModelForm

# add to your views
def feedbackdetails(request, my_id = None):
    if request.method == 'POST':
        form = UserModelForm(request.POST)
        if form.is_valid():
            u = form.save()
            return render(request, 'display.html')

    else:
        obj = AddProgramAndFacultyName.objects.get(id=my_id)
        form_class = UserModelForm(initial={'Program_Name': str(obj.program_name_by_hr),
                                            'Faculty_Name': str(obj.faculty_name_by_hr),
                                            'Date_of_Training': str(obj.Date_of_Training),
                                            'location': str(obj.location_of_training)})

    return render(request, 'formpage.html', {'form': form_class})

def welcome(request):
	return render(request, 'welcome.html')