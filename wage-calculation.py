import openpyxl
from utility.utility import *
import math, os, sys
from datetime import datetime
from tkinter import *
from tkcalendar import Calendar
from pymysql.err import *







global start_datetime_object, end_datetime_object






def select_dates():
    global start_datetime_object, end_datetime_object

    def grad_date():
        global start_datetime_object, end_datetime_object
        start_datetime_object = datetime.strptime(calstart.get_date(), "%m/%d/%y")
        end_datetime_object = datetime.strptime(calend.get_date(), "%m/%d/%y")

        formatted_start_date = start_datetime_object.strftime("%d/%m/%Y")
        formatted_end_date = end_datetime_object.strftime("%d/%m/%Y")
        print(
            f"Date selected (inclusive): {formatted_start_date} to {formatted_end_date}"
        )

        root.destroy()

    root = Tk()
    root.geometry("600x700")

    label1 = Label(root, text="First date to include\n", font=("default", 14))
    label1.pack(pady=10)
    calstart = Calendar(
        root,
        selectmode="day",
        year=datetime.now().year,
        month=datetime.now().month,
        day=datetime.now().day,
    )
    calstart.pack(pady=20)

    label2 = Label(root, text="Last date to include\n", font=("default", 14))
    label2.pack(pady=10)
    calend = Calendar(
        root,
        selectmode="day",
        year=datetime.now().year,
        month=datetime.now().month,
        day=datetime.now().day,
    )
    calend.pack(pady=20)

    Button(root, text="Get Date", command=grad_date).pack(pady=20)
    root.attributes("-topmost", True)
    root.mainloop()




# Main Function for staff-log processing
def TimeWorked():
    def return_results_request():
        connection = return_connection()

        # READ ROLES WAGES FROM SQL
        cursor = connection.cursor()
        query = "SELECT * FROM Clinic.RolesPayment"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

    def WagePerDay(minutes: int, types: str, date: int, patients: int, results):


        roles = {}
        for key_dict in results:
            print(key_dict)
            roles[key_dict['Roles']] = {
                "WeekdayDollar":key_dict["WeekdayDollar"],
                "WeekendDollar":key_dict["WeekendDollar"],
                "OvertimeWeekdayDollar":key_dict["OvertimeWeekdayDollar"],
                "OvertimeWeekendDollar":key_dict["OvertimeWeekendDollar"]
            }

        summation = 0
        summation += 40
        summation += patients


        if patients >= 30:
            summation += 50

        if date < 6:  # weekdays
            time_remaining = max(minutes - 3 * 60, 0) / 30

            summation += roles[types]["WeekdayDollar"]
            summation += (roles[types]["OvertimeWeekdayDollar"] * math.floor(time_remaining))

        if date >= 6:  # weekends
            time_remaining = max(minutes - 4 * 60, 0) / 30

            summation += roles[types]["WeekendDollar"]
            summation += (roles[types]["OvertimeWeekendDollar"] * math.floor(time_remaining))
        
        return summation

    dictionary_of_names_details = {}

    workbook = openpyxl.load_workbook(filename=find_file("staff-log.xlsx"))




    list_of_staff_roles = query_staff_roles()

    for key_dict in list_of_staff_roles:
        print(key_dict)
        dictionary_of_names_details[key_dict['Name']] = {
            'Role':key_dict['Role'], 
            'Payment':0, 
            'Weekdays worked':0, 
            'Weekdays hours':0, 
            'Weekends worked':0, 
            'Weekends hours':0
        }


    input("Input anything to continue")
    os.system("cls")

    print("Select the date range to include in the calculation")
    select_dates()

    requested_results = return_results_request()
    
    print(dictionary_of_names_details)

    for i, row in enumerate(workbook.active.iter_rows(min_row=2, values_only=True), start=2):
        # date, name, clock_in, clock_out, patients = row
        print(row)

        date = row[0]
        try:
            datetime_object = datetime.strptime(date, "%d/%m/%Y")
        except:
            date_now = f"{date.month}/{date.day}/{date.year}"
            datetime_object = datetime.strptime(date_now, "%d/%m/%Y")

        minutes = row[2] * 60
        refer_date = None
        patients = int(row[3])
        paid = 0

        name = row[1]

        if (start_datetime_object <= datetime_object and datetime_object <= end_datetime_object):
            refer_date = (datetime_object.weekday() + 1)  
            # 1 for monday, 7 for sunday, etc
            

            try:
                paid = WagePerDay(
                    minutes, dictionary_of_names_details[name]['Role'], refer_date, patients,requested_results
                )
                if refer_date != None:
                    dictionary_of_names_details[name]['Payment'] += paid
                    
                    if refer_date < 6:
                        dictionary_of_names_details[name]['Weekdays worked'] += 1
                        dictionary_of_names_details[name]['Weekends worked'] += round(minutes / 60.0, 2)
                    if refer_date >= 6:
                        dictionary_of_names_details[name]['Weekends worked'] += 1
                        dictionary_of_names_details[name]['Weekends hours'] += round(minutes / 60.0, 2)
                else:
                    print("Some error somewhere??")
            except KeyError:
                print("Already Quit")

                


            #print(dictionary_of_names_details)
    for x, y in dictionary_of_names_details.items():
        
        if y['Payment'] != 0:

            print(
                f"{x} (Role: {y['Role']}) should be paid {y['Payment']} baht.\nThey worked for {y['Weekdays hours']} weekends for {y['Weekends hours']} hours.\nThey worked for {y['Weekdays worked']} weekdays for {y['Weekdays hours']} hours\n\n"
            )

    input("Input anything to continue")
    sys.exit()


if __name__ == "__main__":
    """
    How this program works:
    - Checks for 2 xlsx files - staff-log and medicine-log (DONE)
    - Creates them if they do not exist (function written) (DONE)
    - Pulls data from sql to xlsx files (modify and check) (OPTION GIVEN)
    - Merge the data for the staff-log. For the medicine-log, no need to do so.

    - Select options: 
        - View staff-log
            - Gives data. Already written
        - View medicine-log 
            - What data to calculate?
            - differentiate between + and -
            - how many used
            - profit, revenue, cost (from usage)
            - stock leftover (first input will be +, starting amount)

    """
    try:
        return_connection()
        TimeWorked()
    except OperationalError:
        print("NO WIFI!")

