import json
import os

FILE_NAME = "attendance.txt"
MINIMUM_ATTENDANCE = 75

students = []


# Load data from file
def load_data():
    global students

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                students = json.load(file)
        except (json.JSONDecodeError, IOError):
            students = []
    else:
        students = []


# Save data to file
def save_data():
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


# Find student by roll number
def find_student(roll):
    for student in students:
        if student["roll"] == roll:
            return student
    return None


# Add a student
def add_student():
    roll = input("Enter roll number: ").strip()

    if not roll.isdigit():
        print("Invalid roll number.")
        return

    if find_student(roll):
        print("Roll number already exists.")
        return

    name = input("Enter student name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    student = {
        "roll": roll,
        "name": name,
        "held": 0,
        "attended": 0
    }

    students.append(student)
    save_data()

    print("Student added successfully!")


# Mark attendance
def mark_attendance():
    roll = input("Enter roll number: ").strip()

    student = find_student(roll)

    if student is None:
        print("Roll number not found.")
        return

    status = input("Enter status (P/A): ").strip().upper()

    if status not in ["P", "A"]:
        print("Invalid status. Enter P or A.")
        return

    student["held"] += 1

    if status == "P":
        student["attended"] += 1

    save_data()

    print("Attendance marked successfully!")


# Calculate attendance percentage
def calculate_percentage(student):
    if student["held"] == 0:
        return 0

    return (student["attended"] / student["held"]) * 100


# Show attendance percentage
def show_percentage():
    roll = input("Enter roll number: ").strip()

    student = find_student(roll)

    if student is None:
        print("Roll number not found.")
        return

    percentage = calculate_percentage(student)

    print(f"\nStudent: {student['name']}")
    print(f"Roll Number: {student['roll']}")
    print(f"Classes Held: {student['held']}")
    print(f"Classes Attended: {student['attended']}")
    print(f"Attendance: {percentage:.2f}%")

    if student["held"] == 0:
        print("No classes held yet.")
    elif percentage >= MINIMUM_ATTENDANCE:
        print("Meets the attendance requirement.")
    else:
        print("Below 75% attendance requirement.")


# Display shortage list
def shortage_list():
    print("\n--- Attendance Shortage List ---")

    found = False

    for student in students:
        percentage = calculate_percentage(student)

        if percentage < MINIMUM_ATTENDANCE:
            found = True
            print(
                f"{student['name']} | Roll: {student['roll']} | "
                f"Attendance: {percentage:.2f}%"
            )

    if not found:
        print("No students below 75% attendance.")


# Display all students
def display_students():
    if not students:
        print("No students found.")
        return

    print("\n--- Student Records ---")

    for student in students:
        percentage = calculate_percentage(student)

        print(
            f"Roll: {student['roll']} | "
            f"Name: {student['name']} | "
            f"Held: {student['held']} | "
            f"Attended: {student['attended']} | "
            f"Percentage: {percentage:.2f}%"
        )


# Main menu
def main():
    load_data()

    while True:
        print("\n===== STUDENT ATTENDANCE MANAGER =====")
        print("1. Add Student")
        print("2. Mark Attendance")
        print("3. Show Attendance Percentage")
        print("4. Shortage List")
        print("5. Display All Students")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            mark_attendance()

        elif choice == "3":
            show_percentage()

        elif choice == "4":
            shortage_list()

        elif choice == "5":
            display_students()

        elif choice == "6":
            save_data()
            print("Data saved. Exiting program.")
            break

        else:
            print("Invalid choice. Please select 1 to 6.")


# Run the program
if __name__ == "__main__":
    main()