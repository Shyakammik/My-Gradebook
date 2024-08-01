import json
import os

class Student:
    def __init__(self, email, names):
        self.email = email
        self.names = names
        self.courses_registered = []
        self.GPA = 0.0

    def calculate_GPA(self):
        if not self.courses_registered:
            self.GPA = 0.0
            return self.GPA

        total_points = 0
        total_credits = 0
        for course, grade in self.courses_registered:
            points = self.grade_to_points(grade) * course['credits']
            total_points += points
            total_credits += course['credits']

        self.GPA = total_points / total_credits if total_credits > 0 else 0.0
        return self.GPA

    @staticmethod
    def grade_to_points(grade):
        grade_mapping = {
            'A': 4.0,
            'B': 3.0,
            'C': 2.0,
            'D': 1.0,
            'F': 0.0
        }
        return grade_mapping.get(grade.upper(), 0.0)

    def register_for_course(self, course, grade):
        self.courses_registered.append({'course': course, 'grade': grade})


class Course:
    def __init__(self, name, trimester, credits):
        self.name = name
        self.trimester = trimester
        self.credits = credits


class GradeBook:
    def __init__(self):
        self.students_file = "students.json"
        self.courses_file = "courses.json"
        self.registrations_file = "registrations.json"
        self.student_list = self.load_json(self.students_file)
        self.course_list = self.load_json(self.courses_file)
        self.registrations = self.load_json(self.registrations_file)

    def load_json(self, filename):
        if os.path.exists(filename):
            with open(filename, "r") as file:
                return json.load(file)
        return []

    def save_json(self, data, filename):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def add_student(self, email, names):
        student = {"email": email, "names": names}
        self.student_list.append(student)
        self.save_json(self.student_list, self.students_file)
        print(f"Student {names} added.")

    def add_course(self, name, trimester, credits):
        course = {"name": name, "trimester": trimester, "credits": credits}
        self.course_list.append(course)
        self.save_json(self.course_list, self.courses_file)
        print(f"Course {name} added.")

    def register_student_for_course(self, email, course_name, grade):
        student = self.find_student_by_email(email)
        course = self.find_course_by_name(course_name)
        if student and course:
            registration = {"email": email, "course_name": course_name, "grade": grade}
            self.registrations.append(registration)
            self.save_json(self.registrations, self.registrations_file)
            print(f"Student {student['names']} registered for course {course_name} with grade {grade}.")
        else:
            print("Student or course not found.")

    def calculate_GPA(self, email):
        student = self.find_student_by_email(email)
        if student:
            student_courses = [reg for reg in self.registrations if reg['email'] == email]
            total_points = 0
            total_credits = 0
            for reg in student_courses:
                course = self.find_course_by_name(reg['course_name'])
                grade = reg['grade']
                points = Student.grade_to_points(grade) * course['credits']
                total_points += points
                total_credits += course['credits']

            GPA = total_points / total_credits if total_credits > 0 else 0.0
            print(f"GPA for {student['names']} is {GPA:.2f}.")
        else:
            print("Student not found.")

    def calculate_ranking(self):
        gpa_list = []
        for student in self.student_list:
            email = student['email']
            student_courses = [reg for reg in self.registrations if reg['email'] == email]
            total_points = 0
            total_credits = 0
            for reg in student_courses:
                course = self.find_course_by_name(reg['course_name'])
                grade = reg['grade']
                points = Student.grade_to_points(grade) * course['credits']
                total_points += points
                total_credits += course['credits']
            GPA = total_points / total_credits if total_credits > 0 else 0.0
            gpa_list.append((student, GPA))

        gpa_list.sort(key=lambda x: x[1], reverse=True)
        for rank, (student, gpa) in enumerate(gpa_list, start=1):
            print(f"Rank {rank}: {student['names']} with GPA {gpa:.2f}")

    def search_by_grade(self, grade):
        result = []
        for reg in self.registrations:
            if reg['grade'] == grade:
                student = self.find_student_by_email(reg['email'])
                course = self.find_course_by_name(reg['course_name'])
                result.append((student, course))

        for student, course in result:
            print(f"Student {student['names']} got grade {grade} in {course['name']}.")

    def generate_transcript(self, email):
        student = self.find_student_by_email(email)
        if student:
            print(f"Transcript for {student['names']}:")
            student_courses = [reg for reg in self.registrations if reg['email'] == email]
            for reg in student_courses:
                course = self.find_course_by_name(reg['course_name'])
                grade = reg['grade']
                print(f"Course: {course['name']}, Trimester: {course['trimester']}, Credits: {course['credits']}, Grade: {grade}")
            self.calculate_GPA(email)
        else:
            print("Student not found.")

    def find_student_by_email(self, email):
        for student in self.student_list:
            if student['email'] == email:
                return student
        return None

    def find_course_by_name(self, name):
        for course in self.course_list:
            if course['name'] == name:
                return course
        return None


def user_interface():
    gradebook = GradeBook()

    while True:
        print("\nMenu:")
        print("1. Add student")
        print("2. Add course")
        print("3. Register student for course")
        print("4. Calculate GPA")
        print("5. Calculate ranking")
        print("6. Search by grade")
        print("7. Generate transcript")
        print("8. Exit")
        choice = input("Choose an action: ")

        if choice == '1':
            email = input("Enter student's email: ")
            names = input("Enter student's name: ")
            gradebook.add_student(email, names)
        elif choice == '2':
            name = input("Enter course name: ")
            trimester = input("Enter course trimester: ")
            credits = int(input("Enter course credits: "))
            gradebook.add_course(name, trimester, credits)
        elif choice == '3':
            email = input("Enter student's email: ")
            course_name = input("Enter course name: ")
            grade = input("Enter grade obtained: ")
            gradebook.register_student_for_course(email, course_name, grade)
        elif choice == '4':
            email = input("Enter student's email: ")
            gradebook.calculate_GPA(email)
        elif choice == '5':
            gradebook.calculate_ranking()
        elif choice == '6':
            grade = input("Enter grade to search: ")
            gradebook.search_by_grade(grade)
        elif choice == '7':
            email = input("Enter student's email: ")
            gradebook.generate_transcript(email)
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    user_interface()
