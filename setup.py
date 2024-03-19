# create database.json
# create staff-names.txt
# create staff-log.xlsx with  Date	Name	Time In	Time Out	Patients Treated
"""
{
    "host":"clinic-program-sql-clinic-program.a.aivencloud.com",
    "password":"AVNS_KhKGSffI6s6ZRqt4Lp6",
    "port":15528,
    "user":"avnadmin",
    "db":"Clinic"
}

staff names -> input and create

staff-log 
Date	Name Time(hours) Patients Treated

"""

from utility.utility import *
import os


database_json = {
    "host":"",
    "password":"",
    "port":1,
    "user":"",
    "db":""
}

make_file(os.getcwd(), "database.json", dump_json=database_json, subdir=False)


print("Input all names. Enter to exit")
names = []
while True:
    name = str(input(":"))
    if name == "":
        break
    names.append(name)
names = "\n".join(names)

if "staff-names.txt" not in os.listdir(os.getcwd()):
    with open("staff-names.txt", "w", encoding="utf-8") as file:
        file.write(names)

xlsx_columns=["Date","Name","Time Worked (Hours)","Patients Treated"]
make_file(os.getcwd(), "staff-log.xlsx",xlsx_columns=xlsx_columns, subdir=False )