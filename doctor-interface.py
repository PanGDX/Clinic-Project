import tkinter as tk
from tkinter import Toplevel
from tkcalendar import Calendar
from datetime import datetime
from tkinter import ttk
from utility.patient_info_request import patient_info
from utility.utility import *
from tkinter import messagebox
import queue
from pymysql.err import OperationalError
next_visit_date = "No Next Visit"


server_running = True
patient_queue_completed = set({})
patient_info_queue = queue.Queue()



def input_info_mom(frame, app):
	def no_next_date():
		if no_next_date_variable.get():
			global next_visit_date
			next_visit_date = "No Next Visit"
			date_label.config(text = next_visit_date)
			


	def delete_form():
		id_entry.delete(0, tk.END)
		name_entry.delete(0, tk.END)
		ga_entry.delete(0, tk.END)
		fh_entry.delete(0, tk.END)
		efw_entry.delete(0, tk.END)
		treatment_note_entry.delete('1.0', tk.END)
		next_visit_ops_entry.delete('1.0', tk.END)
		gyne_doctor_note_entry.delete('1.0', tk.END)
	def on_check_anc():

		gyne_var.set(False)
		other_var.set(False)
	def on_check_gyne():
		anc_var.set(False)

		other_var.set(False)
	def on_check_other():
		anc_var.set(False)
		gyne_var.set(False)




	# Define the function for selecting dates
	def select_dates():
		def grad_date():
			global next_visit_date
			try:
				selected_datetime_object = datetime.strptime(calstart.get_date(), "%m/%d/%y")
				
				next_visit_date = selected_datetime_object.strftime("%d/%m/%Y")

				print(f"Date selected: {next_visit_date}")

				date_label.config(text = next_visit_date)
			except:
				next_visit_date = "No Next Visit"



			date_window.destroy()

		date_window = Toplevel(frame)
		date_window.title("Select Dates")

		calstart = Calendar(date_window, selectmode='day')
		calstart.pack(pady=20)

		select_button = tk.Button(date_window, text="Select Dates", command=grad_date)
		select_button.pack()

	# Define the submit function
	def submit():
		try:
			patient_id = str(id_entry.get())
			patient_name = str(name_entry.get())

			if patient_id == '' or patient_id==None:
				patient_id = query_id_from_name(patient_name)

			if patient_id == None:
				messagebox.showinfo("Error", f"No patient with that ID")
				return
			
			# can this be empty
			ga = ga_entry.get()
			# can this be empty
			fh = fh_entry.get()
			# can this be empty
			efw = efw_entry.get()
			anc_checked = anc_var.get()
			gyne_checked = gyne_var.get()
			other_checked = other_var.get()
			treatment_note = treatment_note_entry.get("1.0", "end-1c")
			
			if not anc_checked and not gyne_checked and not other_checked:
				messagebox.showerror("Error!", "ANC or Gyne not checked")
				return
			elif anc_checked:
				anc_gyne_other = "ANC"
			elif gyne_checked:
				anc_gyne_other = "GYNE"
			elif other_checked:
				anc_gyne_other = "Other"

			next_visit_ops = next_visit_ops_entry.get("1.0", "end-1c")
			gyne_doctor_note = gyne_doctor_note_entry.get("1.0", "end-1c")
			

			data_to_send = {
				"ID":patient_id,
				"First Name":patient_name,
				"GA":ga,
				"FH":fh,
				"EFW":efw,
				"ANC or GYNE":anc_gyne_other,
				"Next Visit Date":next_visit_date,
				"Next Visit Notes":next_visit_ops,
				"Doctor Note":gyne_doctor_note,
				"Treatments + Medicine":treatment_note,
			}
			data_to_log = {
				"GA":ga,
				"FH":fh,
				"EFW":efw,
				"ANC or GYNE":anc_gyne_other,
				"Next Visit Date":next_visit_date,
				"Next Visit Notes":next_visit_ops,
				"Doctor Note":gyne_doctor_note,
				"Treatments + Medicine":treatment_note,
			}


			update_patient_json_using_id(patient_id, data_to_log)

			update_queue_by_mom(data_to_send)
			messagebox.showinfo("Sent", "Completed")

		except Exception as e:
			messagebox.showerror("Error!", "Seems like there was an issue. Check ID and names please.")
			print(e)
		

		# we assume that they are a not a new patient (ie even if they are, already logged at Fai)





	# Create the main window
	id_variables = tk.Frame(frame)
	id_variables.pack(padx=10, pady =5 )
	upper_variables = tk.Frame(frame)
	upper_variables.pack(padx=10, pady=5)

	tk.Label(id_variables, text="ID", font=('Helvetica', 15)).pack(side=tk.LEFT)
	id_entry = tk.Entry(id_variables, font=('Helvetica', 15))
	id_entry.pack(side=tk.LEFT, padx=5)

	tk.Label(id_variables, text="Name", font=('Helvetica', 15)).pack(side=tk.LEFT)
	name_entry = tk.Entry(id_variables, font=('Helvetica', 15))
	name_entry.pack(side=tk.LEFT, padx=5)



	tk.Label(upper_variables, text="GA:",font=('Helvetica', 15) ).pack(side=tk.LEFT)
	ga_entry = tk.Entry(upper_variables, font=('Helvetica', 15))
	ga_entry.pack(side=tk.LEFT, padx=5)

	tk.Label(upper_variables, text="FHR:", font=('Helvetica', 15)).pack(side=tk.LEFT)
	fh_entry = tk.Entry(upper_variables, font=('Helvetica', 15))
	fh_entry.pack(side=tk.LEFT, padx=5)

	tk.Label(upper_variables, text="EFW:", font=('Helvetica', 15)).pack(side=tk.LEFT)
	efw_entry = tk.Entry(upper_variables, font=('Helvetica', 15))
	efw_entry.pack(side=tk.LEFT, padx=5)

	check_box_frame = tk.Frame(upper_variables)
	check_box_frame.pack()

	anc_var = tk.BooleanVar()
	gyne_var = tk.BooleanVar()
	other_var = tk.BooleanVar()
	anc_check = tk.Checkbutton(check_box_frame, text="ANC", variable=anc_var, command=on_check_anc, font=('Helvetica', 15))
	anc_check.pack(side=tk.LEFT, padx=5)
	gyne_check = tk.Checkbutton(check_box_frame, text="Gyne", variable=gyne_var, command=on_check_gyne, font=('Helvetica', 15))
	gyne_check.pack(side=tk.LEFT, padx=5)
	other_check = tk.Checkbutton(check_box_frame, text="Other", variable=other_var, command=on_check_other, font=('Helvetica', 15))
	other_check.pack(side=tk.BOTTOM, padx=5)

	# Pack the button to open the date selection window

	date_frame = tk.Frame(upper_variables)
	date_frame.pack(side= tk.LEFT)

	function_frame = tk.Frame(date_frame)
	function_frame.pack()

	date_button = tk.Button(function_frame, text="Select Next Visit Dates", font=('Helvetica', 15), command=select_dates)
	date_button.pack(padx=10, pady=5, side= tk.LEFT)

	no_next_date_variable = tk.BooleanVar()

	no_next_date_check = tk.Checkbutton(function_frame, text="No Next Visit Date", variable=no_next_date_variable, font=('Helvetica', 15), command=no_next_date)
	no_next_date_check.pack(padx=10, pady=5,side= tk.LEFT)

	date_label = tk.Label(date_frame, text="No dates selected (leave empty if no next appointment)", font=('Helvetica', 15))
	date_label.pack(padx=5, pady=5)






	doctor_note_frame = tk.Frame(frame)
	doctor_note_frame.pack()

	large_input_frame = tk.Frame(frame)
	large_input_frame.pack()
	anc_frame = tk.Frame(large_input_frame)
	anc_frame.pack(side = tk.LEFT)
	next_visit_frame = tk.Frame(large_input_frame)
	next_visit_frame.pack(side = tk.LEFT)

	tk.Label(doctor_note_frame, text="Doctor's Note", font=('Helvetica', 15)).pack(padx=10, pady=5)
	gyne_doctor_note_entry = tk.Text(doctor_note_frame, height=9, width=100,font=('Helvetica', 15))
	gyne_doctor_note_entry.pack(padx=5, pady=5)

	tk.Label(anc_frame, text="Medicines and Treatments for patients", font=('Helvetica', 15)).pack(padx=10, pady=5)
	treatment_note_entry = tk.Text(anc_frame, height=9, width=50, font=('Helvetica', 15))
	treatment_note_entry.pack(padx=5, pady=5)

	# Pack entry widget for Next Visit Operations
	tk.Label(next_visit_frame, text="Next Visit Operations:", font=('Helvetica', 15)).pack(padx=10, pady=5)
	next_visit_ops_entry = tk.Text(next_visit_frame, height=9, width=50, font=('Helvetica', 15))
	next_visit_ops_entry.pack(padx=10, pady=5)

	# Pack the submit button
	button_frames = tk.Frame(frame)
	button_frames.pack()

	submit_button = tk.Button(button_frames, text="Submit", command=submit, font=('Helvetica', 15))
	submit_button.pack(padx=10, pady=10, side = tk.LEFT)

	delete_button = tk.Button(button_frames, text="Clear/Delete all fields", command=delete_form, font=('Helvetica', 15))
	delete_button.pack(padx=10, pady=10, side = tk.LEFT)

	

	app.tab3_id_entry = id_entry
	app.tab3_name_entry = name_entry





class Application(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Doctor Computer")
		self.notebook = ttk.Notebook(self)
		self.notebook.pack(expand=True, fill='both')    


		# Set the window size to the screen size and position it at the top-left corner
		self.state('zoomed')



		self.create_tab1()
		self.create_tab2() 
		self.create_tab3()


	def process_queue(self):

		while not patient_info_queue.empty():
			print("queue is not empty ; removing")
			dict_nameid = patient_info_queue.get_nowait()
			patient_id = str(dict_nameid['ID'])
			patient_name = dict_nameid['First Name']
			patient_queue = dict_nameid['Queue']


			text = f"ID: {patient_id}\nFirst Name: {patient_name}\nQueue Number: {patient_queue}"
			patient_queue_completed.add( (patient_id, patient_name))
			print((patient_id, patient_name))
			self.add_text_frame(dict_nameid, text)


		

	def create_tab1(self):
		self.tab1 = ttk.Frame(self.notebook)
		self.notebook.add(self.tab1, text='Queue')

		refresh_button = tk.Button(self.tab1, text="Refresh Queue", command=self.refresh_queue, font=('Helvetica', 15))
		refresh_button.pack(padx=5, pady=5)

		self.create_scrollable_frame(self.tab1)

	def create_tab2(self):
		self.tab2 = ttk.Frame(self.notebook)
		self.notebook.add(self.tab2, text='Request Patient Information')
		
	
	def create_tab3(self):
		self.tab3 = ttk.Frame(self.notebook)
		self.notebook.add(self.tab3, text='Input Treatment/Medicine')
		
		# Add components to tab2 as needed

	def refresh_queue(self):
		list_of_json_in_string = query_patients_queue_for_mom()
		print("list_of_json_in_string")
		print(list_of_json_in_string)
		if list_of_json_in_string != None:

			for row in list_of_json_in_string:
				patient_id = str(row['ID'])
				patient_name = row['Name']
				if (patient_id, patient_name) not in patient_queue_completed:

					dict_nameid ={"First Name": patient_name, "ID": patient_id}
					patient_info_queue.put(dict_nameid)
					patient_queue_completed.add((patient_id,patient_name))
					
			print("Added!")
			self.process_queue()


	def select_id_and_name(self, id_and_name):
		# Access the input fields in input_info_mom and set their values
		self.tab3_id_entry.delete(0, tk.END)
		self.tab3_id_entry.insert(0, id_and_name['ID'])
		self.tab3_name_entry.delete(0, tk.END)
		self.tab3_name_entry.insert(0, id_and_name['First Name'])

		self.tab2_id_entry.delete(0, tk.END)
		self.tab2_id_entry.insert(0, id_and_name['ID'])
		self.tab2_name_entry.delete(0, tk.END)
		self.tab2_name_entry.insert(0, id_and_name['First Name'])
		
		self.tab2_submit_button.invoke()
		

		
	def create_scrollable_frame(self, parent):
		style = ttk.Style()
		style.configure('TLabel', font=('Helvetica', 15))  # For labels
		style.configure('TButton', font=('Helvetica', 15))  # For buttons




		# Create canvas and scrollbar
		self.canvas = tk.Canvas(parent)
		scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)

		# Pack canvas and scrollbar to fill and expand within the parent frame
		self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		# Configure canvas
		self.canvas.configure(yscrollcommand=scrollbar.set)
		self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

		# Create and add the scrollable frame to the canvas
		self.scrollable_frame = ttk.Frame(self.canvas)
		self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width = self.winfo_screenwidth())

		# Bind mouse scroll events
		self.scrollable_frame.bind("<Enter>", self._bind_mouse_scroll)
		self.scrollable_frame.bind("<Leave>", self._unbind_mouse_scroll)
	def _bind_mouse_scroll(self, event):
		self.canvas.bind_all("<MouseWheel>", self._on_mouse_scroll)

	def _unbind_mouse_scroll(self, event):
		self.canvas.unbind_all("<MouseWheel>")

	def _on_mouse_scroll(self, event):
		self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
	def add_text_frame(self, id_and_name:dict, text):
		# Create a new frame inside the scrollable_frame
		frame = ttk.Frame(self.scrollable_frame)
		frame.pack(fill=tk.BOTH, expand=True)

		
		# Create a frame for buttons
		button_frame = ttk.Frame(frame)
		button_frame.pack(side=tk.TOP, fill=tk.X)

		# Create and pack the Select button in the button frame
		select_button = ttk.Button(button_frame, text="Select", command=lambda: self.select_id_and_name(id_and_name))
		select_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

		# Create and pack the Delete button in the button frame
		delete_button = ttk.Button(button_frame, text="Delete", command=lambda: self.destroy_frame(frame,id_and_name))
		delete_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

		lines = text.split('\n')
		line_count = len(lines)
		# Create a text widget inside the frame
		text_widget = tk.Text(frame, wrap='word', height=line_count+1, font=('Helvetica', 15))
		# text_widget.insert(tk.END, f"ID:{id_and_name['ID']}\nName:{id_and_name['First Name']}\n")
		text_widget.insert(tk.END, text)
		text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
		text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

	def destroy_frame(self,frame, id_and_name):

		patient_queue_completed.add((id_and_name['ID'], id_and_name['First Name']))
		frame.destroy()

	




		

if __name__ == '__main__':
	try:
		delete_previous_days()
		print(query_patients_queue_for_mom())

		app = Application()

		input_info_mom(app.tab3, app)
		patient_info(app.tab2, app)

		def on_closing():
			global server_running
			server_running = False
			app.destroy()
			
		app.protocol("WM_DELETE_WINDOW", on_closing)
		app.mainloop()
	except OperationalError:
		messagebox.showerror("No WIFI!", "No wifi")

		


