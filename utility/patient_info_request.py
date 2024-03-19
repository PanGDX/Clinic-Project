from utility.utility import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont
# only requests information
"""
ID PROMPT   |    NAME PROMPT   |    SUBMIT

SCREEN -> TREEVIEW?

"""
def process_dictionary_to_string(process_dict:dict):
	output_dict = ""

	for key in process_dict:
		if key == 'Name' or key == 'Surname' or key == 'First Name':
			pass
		else:
			if process_dict[key] == None or isinstance(process_dict[key], dict):
				pass
			elif isinstance(process_dict[key], str):
				if len(process_dict[key].split("\n")) == 1:
					output_dict += f"{key}: {process_dict[key]}\n"
				else:
					process_list = process_dict[key].split("\n")
					output_dict += f"{key}:\n"
					for line in process_list:
						output_dict += f"{line}\n"
			else:
				output_dict += f"{key}: {str(process_dict[key])}\n"


	dictionary_strings = ""

	for key in process_dict:
		if key == 'Name' or key == 'Surname' or key == 'First Name':
			pass
		else:
			if isinstance(process_dict[key], dict):
				output_dict += f"\n{key}\n"
				output_dict += process_dictionary_to_string(process_dict[key])
	
	output_dict += f"\n\n{dictionary_strings}"
	return output_dict

def populate_tree(text_box, data:dict):
	# Clear existing tree data
	

	text_box.delete("1.0", tk.END)
	if data == {}:
		return
	else:
		full_output_string = f"Name: {data['First Name']} {data['Surname']}\n"
		string_processed = process_dictionary_to_string(data) 
		full_output_string += string_processed

		print(full_output_string)
		text_box.config(state = "normal")
		text_box.insert("1.0", full_output_string)
		


def patient_info(frame, app =None):

	def submit_process():
		patient_id = id_var.get()
		patient_name = name_var.get()


		if patient_id == "" or patient_id == None:
			patient_id = query_id_from_name(patient_name)
		


		if patient_id != None:
				
			# load patient data
			# update costs into the json file
			json_data = query_patient_info_json_using_id(patient_id)

			if json_data == None:
				populate_tree(text_box, {})
			else:
				
				# query name from ID HERE

				json_data = json.loads(json_data)


				populate_tree(text_box, json_data)
				return
		else:
			populate_tree(text_box, {})
			

		messagebox.showinfo("Error", "Seems like there was an issue. Check ID and names please.")

	id_var = tk.StringVar()
	name_var = tk.StringVar()

	# ID Label and Entry
	style = ttk.Style(frame)

# Configure the Treeview font size
	font = tkFont.Font(family="Helvetica", size=15)  # Change the size as needed
	style.configure("Treeview", font=font)

	input_frame = tk.Frame(frame)
	input_frame.pack(anchor="center", pady=5)

	id_label = tk.Label(input_frame, text="ID: ", font=('Helvetica', 15))
	id_label.pack(side="left")
	id_entry = tk.Entry(
		input_frame,
		textvariable=id_var,
		font=('Helvetica', 15)
	)
	id_entry.pack(side="left", padx=10)

	# Name Label and Entry
	name_label = tk.Label(input_frame, text="First Name: ", font=('Helvetica', 15))
	name_label.pack(side="left")
	name_entry = tk.Entry(input_frame, textvariable=name_var, font=('Helvetica', 15))
	name_entry.pack(side="left")
	
	text_box_frame = tk.Frame(frame,width=600, height=300)
	text_box_frame.pack(fill="both", expand=True)


	text_box = tk.Text(text_box_frame, font=('Helvetica', 15))
	
	text_box.config(state="disabled")  # Disable editing
	text_box.pack(fill="both", expand=True)

	submit_entry = tk.Button(
		frame, width=30, text="Find the patient's information", command=submit_process, font=('Helvetica', 15)
	)
	# submit something. Write function
	submit_entry.pack(pady=20)
	
	if app != None:
		app.tab2_id_entry = id_entry
		app.tab2_name_entry = name_entry
		app.tab2_submit_button = submit_entry


if __name__ == "__main__":
	root = tk.Tk()
	root.geometry("1000x700")
	patient_info(root)
	root.mainloop()
