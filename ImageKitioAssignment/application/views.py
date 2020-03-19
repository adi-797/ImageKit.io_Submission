from django.shortcuts import render
import json, urllib
from datetime import date
from .models import LimitCheck
from django.db.models.base import ObjectDoesNotExist
from .util import getIP
from pymongo import MongoClient

# Global objects for accessing the Mongo Database.
CLIENT = MongoClient("mongodb+srv://adi-797:Hellomongo@mongo1-7hmyo.mongodb.net/test?retryWrites=true&w=majority")

DB = CLIENT["database"]
COLLECTION = DB["UserData"]
# Global object definition ends.

# View function for home page of the application.
def index(request):

	#Obtaining IP Address of the user using a utility function defined in util.py.
	ip = getIP(request)

	# Try and Except block for the case of a new user/IP as no previous record would be there in the SQLlite DB and hence line 24 will throw an error.
	try:
		prev_record = LimitCheck.objects.get(ip_db = ip)

		# limitExceeded variable indicates a user has exhausted the limit of filling the form 3 times in a day.
		# the condition only holds true when previous record for the IP indicate occurrences greater than or equal to 3 for the current day.
		if int(prev_record.occurence_db) > 2 and prev_record.timestamp_db == str(date.today()):
			return render(request, 'index.html', {"limitExceeded":True})

		return render(request, 'index.html')

	# Case for a new user/IP.
	except ObjectDoesNotExist:
		return render(request, 'index.html')
# Definition of index function ends.

# Process_form function for checking the occurrences of the IP and storing the obtained data into a Mongo database.
def process_form(request):
	#Obtaining IP Address of the user using a utility function defined in util.py.
	ip = getIP(request)

	# Retrival of form data using post request.
	captcha = int(request.POST.get('captcha', ''))
	name = str(request.POST.get('name', ''))
	email = str(request.POST.get('email', ''))
	password = str(request.POST.get('password', ''))

	# Case when the user has exhausted the limit of filling the form 3 times in a day so a captcha would be present.
	if captcha:

		# Captcha validation using the Google Recaptcha API.
		recaptcha_response = request.POST.get('g-recaptcha-response')
		url = 'https://www.google.com/recaptcha/api/siteverify'
		values = {
		'secret': "6LdhauIUAAAAACSCxPVY_SC3p0hkn3tLGlDcfyrJ",
		'response': recaptcha_response
		}
		data = urllib.parse.urlencode(values).encode()
		req =  urllib.request.Request(url, data=data)
		response = urllib.request.urlopen(req)
		result = json.loads(response.read().decode())

		# Case when captcha has been submitted successfully.
		if result['success']:

			# Obtaining previous record for the IP. Exception handling is not implemented here as the record would exist for every case ( due to occurrences > 3 ). 
			prev_record = LimitCheck.objects.get(ip_db = ip)

			# Logically there is no need for incrementing the "occurence_db" value.
			# Just for reference; to determine how many times the same IP has filled the form.
			prev_record.occurence_db = str(int(prev_record.occurence_db) + 1)
			prev_record.save()

			# Storing the data in the Mongo DB.
			saveData_perm = {"name_db": name, "email_db": email, "password_db": password, "ip_db": ip}
			COLLECTION.insert_one(saveData_perm)

			return render(request, 'index.html', {"success":True})

		else:
			# Case where user has failed to fill the captcha; requires resubmission.
			return render(request, "index.html", {"captcha_failed":True, "limitExceeded":True})

	# Case when no of occurrences < 3 for the current day.
	else:

		# Exception handling as there exist a case where the entry would be of a new user/ip, so record might not exist and line 90 would throw an error.
		try:
			prev_record = LimitCheck.objects.get(ip_db = ip)

			# There is no need to compare occurrences here for the entry with timestamp matching the current day as it would've gone to the case above ( line 49 ).
			if prev_record.timestamp_db == str(date.today()):
				prev_record.occurence_db = str(int(prev_record.occurence_db) + 1)
				prev_record.save()

			# Case for returning user with occurrences > 3 in any single day previously ( i.e. timestamp doesn't match the current day ).
			else:
				# Updating the timestamp and reinitiating the count for the current day.
				prev_record.occurence_db = "1"
				prev_record.timestamp_db = str(date.today())
				prev_record.save()
				
		# Case for a new entry.
		except ObjectDoesNotExist:
			# Creating entry in the SQLlite DB for the new user/IP.
			new_record = LimitCheck(ip_db = ip, timestamp_db = str(date.today()), occurence_db = "1")
			new_record.save()

		# Storing the data in the Mongo DB.
		saveData_perm = {"name_db": name, "email_db": email, "password_db": password, "ip_db": ip}
		COLLECTION.insert_one(saveData_perm)

		return render(request, 'index.html', {"success":True})
# Definition of Process_form function ends.