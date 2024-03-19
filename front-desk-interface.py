import tkinter as tk
from tkinter import ttk
from utility.utility import *
from tkinter import messagebox
from utility.patient_info_request import patient_info
import queue
from pymysql.err import OperationalError

server_running = True
patient_queue_completed = set({})
patient_info_queue = queue.Queue()


def input_info_fai(frame):
	# Function to retrieve data from the form
	def submit_form():
		try:
			patient_id = id_entry.get()
			patient_name =  name_entry.get()
			queue_number = queue_number_label.get()

			data_to_log_if_new = {
				"First Name" : name_entry.get(),
				"Surname" : surname_entry.get(),
				"Workplace Name": workplace_entry.get(),
				"Insurance Type": insurance_var.get(),
			}

			# new data every single time
			data_to_log = {
				"Age": float(age_entry.get()),
				"Blood Pressure": int(bp_entry.get()),
				"Weight": float(weight_entry.get()),
				"Urine Protein/Sugar": float(urine_entry.get()),
				"Additional Details": details_entry.get("1.0", "end-1c")
			}
		except:
			messagebox.showerror("Error!", "Seems like there was an issue. Check values please.")



		if patient_id == '' or patient_id==None:
			patient_id = query_id_from_name(patient_name)
		

		patient_name_from_sql = query_name_from_id(patient_id)


		if patient_id == None:        
			messagebox.showinfo("Error", f"No patient with that ID")
			return
		

		else:
			if patient_name_from_sql == None: # New patient
				if patient_name != "" and patient_name != None:
					update_name_2_id(patient_name,patient_id)
					update_patient_json_using_id_first_time(patient_id, data_to_log_if_new)

					update_patient_json_using_id(patient_id, data_to_log)
					
					update_queue_by_fai(patient_id,patient_name,queue_number)

					messagebox.showinfo("Done", "Logged and updated ID of patient with no issues")
					
					return
			else:
				update_patient_json_using_id(patient_id, data_to_log)
				
				update_queue_by_fai(patient_id,patient_name,queue_number)

				messagebox.showinfo("Done", "Logged with no issues")
		
				return
		messagebox.showinfo("Error", "Seems like there was an issue. Check ID and names please.")

	def delete_form():
		id_entry.delete(0, tk.END)
		name_entry.delete(0, tk.END)
		surname_entry.delete(0, tk.END)
		age_entry.delete(0, tk.END)
		bp_entry.delete(0, tk.END)
		weight_entry.delete(0, tk.END)
		urine_entry.delete(0, tk.END)
		workplace_entry.delete(0, tk.END)
		details_entry.delete('1.0', tk.END)

	id_label = tk.Label(frame, text="ID", font=('Helvetica', 15))
	id_label.grid(row=0, column=0, padx=5, pady=5)
	id_entry = tk.Entry(frame, font=('Helvetica', 15))
	id_entry.grid(row=0, column=1, padx=5, pady=5)


	# Create and place form elements
	# Name
	name_label = tk.Label(frame, text="Name", font=('Helvetica', 15))
	name_label.grid(row=1, column=0, padx=5, pady=5)
	name_entry = tk.Entry(frame, font=('Helvetica', 15))
	name_entry.grid(row=1, column=1, padx=5, pady=5)

	# Surname
	surname_label = tk.Label(frame, text="Surname", font=('Helvetica', 15))
	surname_label.grid(row=2, column=0, padx=5, pady=5)
	surname_entry = tk.Entry(frame, font=('Helvetica', 15))
	surname_entry.grid(row=2, column=1, padx=5, pady=5)

	# Age
	age_label = tk.Label(frame, text="Age", font=('Helvetica', 15))
	age_label.grid(row=3, column=0, padx=5, pady=5)
	age_entry = tk.Entry(frame, font=('Helvetica', 15))
	age_entry.grid(row=3, column=1, padx=5, pady=5)

	# Blood Pressure
	bp_label = tk.Label(frame, text="Blood Pressure", font=('Helvetica', 15))
	bp_label.grid(row=4, column=0, padx=5, pady=5)
	bp_entry = tk.Entry(frame, font=('Helvetica', 15))
	bp_entry.grid(row=4, column=1, padx=5, pady=5)

	# Weight
	weight_label = tk.Label(frame, text="Weight", font=('Helvetica', 15))
	weight_label.grid(row=5, column=0, padx=5, pady=5)
	weight_entry = tk.Entry(frame, font=('Helvetica', 15))
	weight_entry.grid(row=5, column=1, padx=5, pady=5)

	# Urine Protein/Sugar
	urine_label = tk.Label(frame, text="Urine Protein/Sugar", font=('Helvetica', 15))
	urine_label.grid(row=6, column=0, padx=5, pady=5)
	urine_entry = tk.Entry(frame, font=('Helvetica', 15))
	urine_entry.grid(row=6, column=1, padx=5, pady=5)

	# Workplace Name
	workplace_label = tk.Label(frame, text="Workplace Name", font=('Helvetica', 15))
	workplace_label.grid(row=7, column=0, padx=5, pady=5)
	workplace_entry = tk.Entry(frame, font=('Helvetica', 15))
	workplace_entry.grid(row=7, column=1, padx=5, pady=5)

	# Insurance Type
	insurance_label = tk.Label(frame, text="Insurance Type", font=('Helvetica', 15))
	insurance_label.grid(row=8, column=0, padx=5, pady=5)
	insurance_var = tk.StringVar()
	insurance_options = ["Public", "Private", "None", "Other"]
	insurance_menu = ttk.Combobox(frame, textvariable=insurance_var, values=insurance_options, font=('Helvetica', 15))
	insurance_menu.grid(row=8, column=1, padx=5, pady=5)
	insurance_menu.current(0)


	queue_number_label = tk.Label(frame, text="Queue Number", font=('Helvetica', 15))
	queue_number_label.grid(row=9, column=0, padx=5, pady=5)
	queue_number_entry = tk.Entry(frame, font=('Helvetica', 15))
	queue_number_entry.grid(row=9, column=1, padx=5, pady=5)

	# Additional Details
	details_label = tk.Label(frame, text="Additional Details", font=('Helvetica', 15))
	details_label.grid(row=10, column=0, padx=5, pady=5)
	details_entry = tk.Text(frame, height=4, width=30, font=('Helvetica', 15))
	details_entry.grid(row=10, column=1, padx=5, pady=5)

	# Submit Button
	submit_button = tk.Button(frame, text="Submit", command=submit_form, font=('Helvetica', 15))
	submit_button.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

	clear_button = tk.Button(frame, text="Clear/Delete all fields", command=delete_form, font=('Helvetica', 15))
	clear_button.grid(row=12, column=0, columnspan=2, padx=5, pady=5)
	# Start the application




class Application(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Front Desk Computer")
		self.notebook = ttk.Notebook(self)
		self.notebook.pack(expand=True, fill='both')

		# Set the window size to the screen size and position it at the top-left corner
		self.state('zoomed')



		self.create_tab1()
		self.create_tab2()
		self.create_tab3()

		self.refresh_queue()

		
	def process_queue(self):

		while not patient_info_queue.empty():
			print("queue is not empty ; removing")
			json_information = patient_info_queue.get_nowait()
			#print(json_information)

			patient_id = str(json_information['ID'])
			patient_name = json_information['First Name']
			next_visit_date = json_information['Next Visit Date']
			next_visit_treatment = json_information['Next Visit Notes']


			text = f"ID: {patient_id}\nFirst Name: {patient_name}\nNext Visit Date:{next_visit_date}\nNext Visit Treatment:\n{next_visit_treatment}"
			print(text)

			patient_queue_completed.add( (patient_id, patient_name))
			print((patient_id, patient_name))
			self.add_text_frame(text)



	def create_tab1(self):
		self.tab1 = ttk.Frame(self.notebook)
		self.notebook.add(self.tab1, text='Input Patient Information')

		input_info_fai(self.tab1)
		

	def create_tab2(self):
		self.tab2 = ttk.Frame(self.notebook)
		self.notebook.add(self.tab2, text='Request Patient Information')
		
		patient_info(self.tab2)
		# Add components to tab2 as needed

	def create_tab3(self):
		self.tab3 = ttk.Frame(self.notebook)
		self.notebook.add(self.tab3, text = "Checkout Queue")

		refresh_button = tk.Button(self.tab3, text="Refresh Queue", command=self.refresh_queue, font=('Helvetica', 15))
		refresh_button.pack(padx=5, pady=5)

		self.create_scrollable_frame(self.tab3)

	def refresh_queue(self):
		list_of_json_in_string = query_patients_queue_for_staff()
		print("list_of_json_in_string")
		print(list_of_json_in_string)
		if list_of_json_in_string != None:
			for row in list_of_json_in_string:
				patient_id = str(row['ID'])
				patient_name = row['Name']
				if (patient_id, patient_name) not in patient_queue_completed:
					json_information = json.loads(row['Json'])
					patient_info_queue.put(json_information)
					patient_queue_completed.add((patient_id,patient_name))
			print("Added!")
			self.process_queue()
	def create_scrollable_frame(self, parent):
		style = ttk.Style()
		style.configure('TLabel', font=('Helvetica', 15))  # For labels
		style.configure('TButton', font=('Helvetica', 15))  # For buttons
		
		self.canvas = tk.Canvas(parent)
		self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		self.canvas.configure(yscrollcommand=scrollbar.set)
		self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

		self.scrollable_frame = ttk.Frame(self.canvas)
		self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width = self.winfo_screenwidth())

		self.scrollable_frame.bind("<Enter>", self._bind_mouse_scroll)
		self.scrollable_frame.bind("<Leave>", self._unbind_mouse_scroll)
	def _bind_mouse_scroll(self, event):
		self.canvas.bind_all("<MouseWheel>", self._on_mouse_scroll)

	def _unbind_mouse_scroll(self, event):
		self.canvas.unbind_all("<MouseWheel>")

	def _on_mouse_scroll(self, event):
		self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
	def add_text_frame(self, text):
		# Create a new frame inside the scrollable_frame
		frame = ttk.Frame(self.scrollable_frame)
		frame.pack(fill=tk.BOTH, expand=True)

		# Create a delete button at the top of the frame
		delete_button = ttk.Button(frame, text="Delete", command=lambda: frame.destroy())
		delete_button.pack(side=tk.TOP, fill=tk.X)

		# Create a text widget inside the frame

		lines = text.split('\n')
		line_count = len(lines)

		text_widget = tk.Text(frame, wrap='word', height=line_count + 1, font=('Helvetica', 15))
		text_widget.insert(tk.END, text)
		text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
		text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



	




		

if __name__ == '__main__':
	try:
		delete_previous_days()
		app = Application()

		def on_closing():
			global server_running
			server_running = False
			app.destroy()
		app.protocol("WM_DELETE_WINDOW", on_closing)
		app.mainloop()
	except OperationalError:
		messagebox.showerror("No WIFI!", "No wifi")




