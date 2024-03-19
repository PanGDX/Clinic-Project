# Set up
### System requirements
- Python 3
- MySQL server 



### Commands
`pip install -r requirements.txt` 
`python setup.py`

# Program Descriptions
### `old-login-interface.py`
Used by the workers to indicate when their shift starts and when they leave their shift
![Image](Documentation/Old-Checkin/1.png)



### `new-login.py`
Used by the workers to indicate when their shift starts and when they leave their shift
![Image](Documentation/New-Checkin/1.png)
![Image](Documentation/New-Checkin/2.png)

### `front-desk-inferface.py`
- Search for information of the patient using name/ID
- Displays a list of patients and their next treatment date
- User can log new and existing patient information into the database
![Image](Documentation/Front-Desk/1.png)


### `payment-interface.py`
- Search for information of the patient using name/ID
- Displays a list of patients and their prescribed medicine and treatments for the user to use and calculate for payment collection
![Image](Documentation/Payment-Desk/1.png)

### `doctor-interface.py`
- Search for information of the patient using name/ID
- Prescribe medicine and treatments, type out notes and set the next appointment through a simple GUI
![Image](Documentation/Doctor-Desk/1.png)
![Image](Documentation/Doctor-Desk/2.png)


### `wage-calculation.py`
Calculate the wage that each worker should be paid over a range of days through CLI



### `settings.py`
Modify the settings by updating MySQL database
![Image](Documentation/Settings/1.png)
![Image](Documentation/Settings/2.png)