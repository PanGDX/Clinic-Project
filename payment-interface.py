import tkinter as tk
from tkinter import ttk
from utility.utility import *
from tkinter import messagebox
import queue
from utility.patient_info_request import patient_info
from pymysql.err import OperationalError

server_running = True
patient_queue_completed = set({})
patient_info_queue = queue.Queue()


class Application(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Payment Computer")
		self.notebook = ttk.Notebook(self)
		self.notebook.pack(expand=True, fill='both')    


		# Set the window size to the screen size and position it at the top-left corner
		self.state('zoomed')

		self.create_tab1()
		self.create_tab2() 

		self.refresh_queue()


	def process_queue(self):

		while not patient_info_queue.empty():
			print("queue is not empty ; removing")
			json_information = patient_info_queue.get_nowait()
			
			patient_id = str(json_information['ID'])
			patient_name = json_information['First Name']
			treatments_and_meds = json_information['Treatments + Medicine']

			dict_nameid ={"First Name": patient_name, "ID": patient_id}
			text = f"ID: {patient_id}\nFirst Name: {patient_name}\nTreatments and Medicines:\n{treatments_and_meds}"
			print(text)
			patient_queue_completed.add( (patient_id, patient_name))
			print((patient_id, patient_name))
			self.add_text_frame(dict_nameid, text)
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
	def check_queue(self):
		print("Checking queue")
		self.process_queue()
		self.after(1000 * 10, self.check_queue)  # Schedule the next queue check


	def select_id_and_name(self, id_and_name):

		self.tab2_id_entry.delete(0, tk.END)
		self.tab2_id_entry.insert(0, id_and_name['ID'])
		self.tab2_name_entry.delete(0, tk.END)
		self.tab2_name_entry.insert(0, id_and_name['First Name'])

		self.tab2_submit_button.invoke()

		patient_queue_completed.add((id_and_name['ID'], id_and_name['First Name']))

	def create_tab1(self):
		self.tab1 = ttk.Frame(self.notebook)
		self.notebook.add(self.tab1, text='Checkout Queue')

		refresh_button = tk.Button(self.tab1, text="Refresh Queue", command=self.refresh_queue, font=('Helvetica', 15))
		refresh_button.pack(padx=5, pady=5)

		self.create_scrollable_frame(self.tab1)

	def create_tab2(self):
		self.tab2 = ttk.Frame(self.notebook)
		self.notebook.add(self.tab2, text='Request Patient Information')
		
		# Add components to tab2 as needed

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
		text_widget = tk.Text(frame, wrap='word', height=line_count + 1, font=('Helvetica', 15))
		# text_widget.insert(tk.END, f"ID:{id_and_name['ID']}\nFirst Name:{id_and_name['First Name']}\n")
		text_widget.insert(tk.END, text)
		text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
		text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
	def destroy_frame(self,frame, id_and_name):

		patient_queue_completed.add((id_and_name['ID'], id_and_name['First Name']))
		frame.destroy()


	




		

if __name__ == '__main__':
		
	try:
		delete_previous_days()
		app = Application()


		patient_info(app.tab2, app)

		def on_closing():		
			global server_running
			server_running = False
			app.destroy()
		app.protocol("WM_DELETE_WINDOW", on_closing)
		app.mainloop()
	except OperationalError:
		messagebox.showerror("No WIFI!", "No wifi")



