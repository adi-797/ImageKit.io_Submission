from pymongo import MongoClient
import csv

CLIENT = MongoClient("mongodb+srv://adi-797:Hellomongo@mongo1-7hmyo.mongodb.net/test?retryWrites=true&w=majority")

DB = CLIENT["database"]
COLLECTION = DB["UserData"]

db_obj = COLLECTION.find()

header = ['Index', 'Name', 'Email', 'Password', 'IP Address']
empty_row = ['','','','','']
	
with open("UserData.csv", 'w') as csv_file:
    writer = csv.writer(csv_file)

    writer.writerow(header)
    writer.writerow(empty_row)

    for row in db_obj:
        writer.writerow([element for element in row.values()])

csv_file.close()
