from django.test import TestCase

# Create your tests here.
from django.urls import path
from django.conf import settings

from feedbackapp import views as feedbackapp_views

urlpatterns = [
  path('feedbackdetails/<int:my_id>', feedbackapp_views.feedbackdetails),
  path('display/', feedbackapp_views.feedbackdetails),
  path('', feedbackapp_views.welcome),
 ]