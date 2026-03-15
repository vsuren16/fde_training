#### HOSPITAL PATIENT APPOINTMENT ANALYZER ####

#importing modules
from appointments import store_appointments
from appointments import display_appointments
from appointments import filter_by_department

#Initializing variable
i=0
patient_appointment_details_list = []

#calling appointment function
appointment_nos = store_appointments()

#Looping to get and store patient details
while i < appointment_nos: 
            
    print(f"\nAppointment {i+1}:")

    patient_details_tup  = []

    patient_name = input("Please enter patient name: ")
    patient_city = input("Please enter patient city: ")
    patient_dept = input("Please enter patient department: ")

    patient_details_tup = (patient_name,patient_city,patient_dept)
    patient_appointment_details_list.append(patient_details_tup)
    i = i+1

#displaying all patient details
dis = display_appointments(patient_appointment_details_list)

#filtering the patients by department
patient_filter_dept = input("\nEnter department to filter: ")
filtered_patients = filter_by_department(patient_filter_dept, patient_appointment_details_list)

#printing the final filtered patients details
if filtered_patients:

    for patient_name,patient_city,patient_dept in filtered_patients:
        print(f"\nPatients with {patient_dept} Appointments:")
        print("--------------------------------------------")
        print(f"Name: {patient_name}")
        print(f"City: {patient_city}")
        print("--------------------------------------------")
else:
    print(f"\nPatients with {patient_filter_dept} Appointments:")
    print("--------------------------------------------")
    print("No appoitments found.")
    print("--------------------------------------------")

