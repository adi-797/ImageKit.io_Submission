from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('process_form', views.process_form, name="process_form"),
	path('viewdata', views.viewdata, name="viewdata"),
	path('erase', views.erase, name="erase")
]