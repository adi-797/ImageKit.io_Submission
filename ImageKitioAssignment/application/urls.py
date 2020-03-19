from django.urls import path
from django.conf.urls import url
from . import views

# URL definitions for the application. Has only two urls, the home page at 127.0.0.1:8000 (local host) and "process_form" for form submission.
urlpatterns = [
	path('', views.index, name='index'),
	path('process_form', views.process_form, name="process_form"),
]