# INVESTIGATORY PROJECT
import tkinter as tk
from tkinter import ttk
import mysql.connector

# MySQL connection setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Sakila*2root",
    database="thanusree"
)

cursor = db.cursor()

# Function to create the table if not exists
def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS HealthRecords (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Name VARCHAR(255),
            Surname VARCHAR(255),
            Age INT,
            Gender VARCHAR(10),
            BloodType VARCHAR(10),
            Height FLOAT,
            Weight FLOAT,
            BMI FLOAT,
            BloodPressure VARCHAR(20),
            DOB DATE,
            VisionScreening VARCHAR(10),
            RightEye VARCHAR(10),
            LeftEye VARCHAR(10),
            RightEar VARCHAR(10),
            LeftEar VARCHAR(10)
        )
    """)
    db.commit()

# ...

# Function to add a basic health record
# Function to add a basic health record
def add_basic_health_details(record):
    print("\nAdding Health Details:")
    record['Height'] = float(input("Enter height (in cm): "))
    record['Weight'] = float(input("Enter weight (in kg): "))
    record['BMI'] = record['Weight'] / ((record['Height'] / 100) ** 2)
    print(f"BMI: {record['BMI']}")

    record['BloodPressure'] = input("Enter blood pressure (e.g., 120/80): ")
    record['DOB'] = input("Enter date of birth (YYYY-MM-DD): ")

    # Add VisionScreening to the record dictionary
    record['VisionScreening'] = ''

    # Return the updated details
    return record




# Function for physical examination
# Function for physical examination
def physical_examination(record):
    record_dict = {
        'VisionScreening': record.get('VisionScreening', ''),  
        'RightEye': record.get('RightEye', ''),
        'LeftEye': record.get('LeftEye', ''),
        'RightEar': record.get('RightEar', ''),
        'LeftEar': record.get('LeftEar', '')
    }

    print("\nPerforming Physical Examination:")
    record_dict['VisionScreening'] = input("Vision screening: ")
    record_dict['RightEye'] = input("Right Eye: ")
    record_dict['LeftEye'] = input("Left Eye: ")

    print("\nHearing Screening:")
    record_dict['RightEar'] = input("Right Ear: Pass/Fail: ")
    record_dict['LeftEar'] = input("Left Ear: Pass/Fail: ")

    return record_dict





# Function to add a basic student details
def add_record():
    n = input("Enter student's name: ")
    s_n = input("Enter student's surname: ")
    a = int(input("Enter student's age: "))
    g = input("Enter student's gender: ")
    b = input("Enter student's blood type: ")

    # Create a dictionary for the basic health record
    record = {'Name': n, 'Surname': s_n, 'Age': a, 'Gender': g, 'BloodType': b}
    record.update(add_basic_health_details(record))
    record.update(physical_examination(record))

    # Insert data into MySQL table
    cursor.execute("""
        INSERT INTO HealthRecords (Name, Surname, Age, Gender, BloodType, Height, Weight, BMI,
        BloodPressure, DOB, VisionScreening, RightEye, LeftEye, RightEar, LeftEar)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        record['Name'], record['Surname'], record['Age'], record['Gender'], record['BloodType'],
        record['Height'], record['Weight'], record['BMI'], record['BloodPressure'], record['DOB'],
        record['VisionScreening'], record['RightEye'], record['LeftEye'], record['RightEar'], record['LeftEar']
    ))

    db.commit()
    print("Record added successfully!\n")



# Function to view all health records
def view_records():
    cursor.execute("SELECT * FROM HealthRecords")
    records = cursor.fetchall()

    if not records:
        print("No records available.")
    else:
        print("Health Records:")
        for record in records:
            print(f"Name: {record[1]}, Surname: {record[2]}, Age: {record[3]}, Gender: {record[4]}, Blood Type: {record[5]}")

        print()

# Function to search for a health record by name
def search_record():
    search = input("Enter the name to search: ")
    cursor.execute("SELECT * FROM HealthRecords WHERE Name = %s", (search,))
    record = cursor.fetchone()

    if record:
        print("Record found:")
        print(f"Name: {record[1]}, Age: {record[3]}, Gender: {record[4]}, Blood Type: {record[5]}")
    else:
        print("Record not found.\n")

# Function to delete a health record
def delete_record():
    name_to_delete = input("Enter the name to delete: ")
    cursor.execute("DELETE FROM HealthRecords WHERE Name = %s", (name_to_delete,))
    db.commit()
    print(f"Record for {name_to_delete} deleted successfully!\n")
# ...
    
    
# Create a tkinter window
root = tk.Tk()
root.title("Student Health Record Management System")
root.geometry("600x400")  # Set the window size
root.configure(background='#FFE4C4')  # Set background color


# Create a style to configure colors
style = ttk.Style()
style.configure("TButton", foreground="BLACK", background="#CD9B9B")
style.configure("TLabel", foreground="black", background="#FFE4C4")

# Create and place widgets in the tkinter window
label = ttk.Label(root, text="Student Health Record Management System",font=('Times New Roman',30,'bold'),border=12)
label.pack(pady=10)

button_add = ttk.Button(root, text="Add Basic Record", command=add_record)
button_add.pack(pady=5)

button_view = ttk.Button(root, text="View Records", command=view_records)
button_view.pack(pady=5)

button_search = ttk.Button(root, text="Search Record", command=search_record)
button_search.pack(pady=5)

button_delete = ttk.Button(root, text="Delete Record", command=delete_record)
button_delete.pack(pady=5)



button_exit = ttk.Button(root, text="Exit", command=root.destroy)
button_exit.pack(pady=5)

# Initialize the database table
create_table()

# Start the tkinter main loop
root.mainloop()


# Initialize the database table
create_table()

# Start the tkinter main loop
root.mainloop()
