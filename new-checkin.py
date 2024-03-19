import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import datetime
from utility.utility import find_file,remove_blank_rows
from openpyxl import load_workbook

def load_names():
	try:
		with open('del-names.json', 'r') as file:
			return json.load(file)
	except FileNotFoundError:
		return {}

def save_names(names):
	with open('del-names.json', 'w') as file:
		json.dump(names, file)

def update_name_list():
	today_str = datetime.datetime.now().strftime("%d/%m/%Y")
	existing_names = names.get(today_str, [])
	name_list.delete(0, tk.END)
	for name in all_names:
		if name not in existing_names:
			name_list.insert(tk.END, name)

def add_name(event=""):
	name_index = name_list.curselection()
	if name_index:
		name = name_list.get(name_index)
		login_popup(name)
	else:
		messagebox.showinfo("No names selected", "No names selected")

def login_popup(name):
	def submit():
		try:
			hours = hours_entry.get()
			minutes = minutes_entry.get()
			patients = patient_entry.get()

			if minutes == "":
				minutes = 0
			else:
				minutes = int(minutes)
			if hours == "":
				hours = 0
			else:
				hours = int(hours)
			if patients == "":
				patients = 0
			else:
				patients = int(patients)
		except:
			messagebox.showinfo("Not a number", "Not a number")

		hours = hours + minutes/60
		record_work(name, hours, patients)
		popup.destroy()

	popup = tk.Toplevel(root)
	popup.title("Record Work Hours")

	tk.Label(popup, font = ('Helvetica', 15), text=f"Name: {name}").pack()
	tk.Label(popup, font = ('Helvetica', 15), text="Hours Worked:").pack()
	hours_entry = tk.Entry(popup, font = ('Helvetica', 15))
	hours_entry.pack()
	tk.Label(popup, text="Minutes Worked:", font = ('Helvetica', 15)).pack()
	minutes_entry = tk.Entry(popup, font = ('Helvetica', 15))
	minutes_entry.pack()
	tk.Label(popup, text="Patients Treated:", font = ('Helvetica', 15)).pack()
	patient_entry = tk.Entry(popup, font = ('Helvetica', 15))
	patient_entry.pack()
	
	submit_btn = tk.Button(popup, text="Submit", command=submit, font = ('Helvetica', 15))
	submit_btn.pack()

def record_work(name, hours=0, patients=0):
	workbook = load_workbook(filename=log_location)

	today_str = datetime.datetime.now().strftime("%d/%m/%Y")
	if today_str not in names:
		names[today_str] = []
	names[today_str].append(name)
	save_names(names)
	update_name_list()

	now = datetime.datetime.now()
	date = now.strftime("%d/%m/%Y")

	if now.minute < 10:
		time = f"{now.hour}:0{now.minute}"
	else:
		time = f"{now.hour}:{now.minute}"

	messagebox.showinfo("Clock In", f"{name} logged in at {date} {time}")
	workbook.active.append([date, name, hours, patients])
	workbook.save(filename=log_location)
	workbook.close()



def on_closing():
	today_str = datetime.datetime.now().strftime("%d/%m/%Y")
	for date in list(names.keys()):
		if date != today_str:
			del names[date]
	save_names(names)
	root.destroy()





if __name__ == '__main__':
	log_location = find_file('staff-log.xlsx')
	remove_blank_rows(log_location)


	root = tk.Tk()
	root.title("Work Login System")
	root.geometry("500x700")

	names = load_names()
	with open(find_file('staff-names.txt'), "r", encoding = "utf-8") as file:
		all_names = (file.read()).split("\n")

	name_list = tk.Listbox(root, font = ('Helvetica', 15), height=20)
	name_list.pack(pady="5px", padx = "5px", fill="x")
	name_list.bind('<Double-1>', add_name)

	popup_btn = tk.Button(root, text="Check In", command=add_name, font = ('Helvetica', 15))
	popup_btn.pack()

	update_name_list()

	root.protocol("WM_DELETE_WINDOW", on_closing)
	root.mainloop()
