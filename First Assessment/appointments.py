### THIS MODULE IS USED IN HOSPITAL PATIENT APPOINTMENT ANALYZER JOB ####

def store_appointments():

    appointment_nos = int(input("Enter number of appointments: "))
    return appointment_nos


def display_appointments(patient_appointment_details_list):

    for patient_name,patient_city,patient_dept in patient_appointment_details_list:
        print("--------------------------------------------")
        print(f"Patient Name: {patient_name}")
        print(f"City: {patient_city}")
        print(f"Department: {patient_dept}") 
        print("--------------------------------------------")

def filter_by_department(patient_filter_dept, patient_appointment_details_list):
    result = []
    for dept in patient_appointment_details_list:
        if dept[2] == patient_filter_dept:
            result.append(dept)
    return result







