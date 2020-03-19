from django.shortcuts import render
import json, urllib
from datetime import date
from .models import LimitCheck
from django.db.models.base import ObjectDoesNotExist
from .util import getIP
from pymongo import MongoClient

# Create your views here.

CLIENT = MongoClient("mongodb+srv://adi-797:Hellomongo@mongo1-7hmyo.mongodb.net/test?retryWrites=true&w=majority")

DB = CLIENT["database"]
COLLECTION = DB["UserData"]

def index(request):
	ip = getIP(request)

	try:
		prev_record = LimitCheck.objects.get(ip_db = ip)

		if int(prev_record.occurence_db) > 2 and prev_record.timestamp_db == str(date.today()): #Same day with >3 occurences only; otherwise normal.
			return render(request, 'index.html', {"limitExceeded":True})

		return render(request, 'index.html')

	except ObjectDoesNotExist:
		return render(request, 'index.html')

def process_form(request):
	ip = getIP(request)

	captcha = int(request.POST.get('captcha', ''))

	name = str(request.POST.get('name', ''))
	email = str(request.POST.get('email', ''))
	password = str(request.POST.get('password', ''))

	if captcha:
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

		if result['success']:

			prev_record = LimitCheck.objects.get(ip_db = ip)

			print ("########### SAME DATE >3 OCC")
			prev_record.occurence_db = str(int(prev_record.occurence_db) + 1) #just for reference; to determine how many times the same IP has filled the form.
			prev_record.save()

			saveData_perm = {"name_db": name, "email_db": email, "password_db": password, "ip_db": ip}
			COLLECTION.insert_one(saveData_perm)

			return render(request, 'index.html', {"success":True})

		else:
			return render(request, "index.html", {"captcha_failed":True, "limitExceeded":True})
	else:
		try:
			prev_record = LimitCheck.objects.get(ip_db = ip)

			if prev_record.timestamp_db == str(date.today()): #No need to compare occurences as it would've gone to the above case for >3.
				print ("########### SAME USER LESS OCC SAME DATE")
				prev_record.occurence_db = str(int(prev_record.occurence_db) + 1)
				prev_record.save()

			else:
				print ("########### SAME USER ANY OCC OLD DATE") #returning user with >3 occurences in any single day.
				prev_record.occurence_db = "1"
				prev_record.timestamp_db = str(date.today())
				prev_record.save()
				
		except ObjectDoesNotExist:
			print ("########### NEW CASE")
			new_record = LimitCheck(ip_db = ip, timestamp_db = str(date.today()), occurence_db = "1")
			new_record.save()

		saveData_perm = {"name_db": name, "email_db": email, "password_db": password, "ip_db": ip}
		COLLECTION.insert_one(saveData_perm)

		return render(request, 'index.html', {"success":True})

def viewdata(request):
	all_data = UserData.objects.all()
	data_list = [str(element) for element in list(all_data)]
	final_data = [element.split('#') for element in data_list]

	print ("USer\n", final_data, "\n\n\n")

	all_data = LimitCheck.objects.all()
	data_list = [str(element) for element in list(all_data)]
	final_data = [element.split('#') for element in data_list]

	print (final_data, "\n\n\n")

	return render(request, 'index.html', {"success":True})

def erase(request):
	all_data = UserData.objects.all()
	all_data.delete()
	all_data = LimitCheck.objects.all()
	all_data.delete()


	# x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	# if x_forwarded_for:
	# 	ip = x_forwarded_for.split(',')[-1].strip()
	# else:
	# 	ip = request.META.get('REMOTE_ADDR')

	# c = LimitCheck.objects.get(ip_db = ip)
	# c.timestamp_db = "2020-02-19"
	# c.save()
	return render(request, 'index.html', {"success":True})