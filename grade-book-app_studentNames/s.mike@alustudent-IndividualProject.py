#!/usr/bin/python3

### Enhanced Code

python3
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
        else:
            total_points = sum(course['credits'] * course['grade'] for course in self.courses_registered)
            total_credits = sum(course['credits'] for course in self.courses_registered)
            self.GPA = total_points / total_credits

    def register_for_course(self, course, grade):
        self.courses_registered.append({"course": course, "credits": course.credits, "grade": grade})
        self.calculate_GPA()

    def to_dict(self):
        return {
            "email": self.email,
            "names": self.names,
            "courses_registered": self.courses_registered,
            "GPA": self.GPA
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(data['email'], data['names'])
        student.courses_registered = data['courses_registered']
        student.GPA = data['GPA']
        return student

class Course:
    def __init__(self, name, trimester, credits):
        self.name = name
        self.trimester = trimester
        self.credits = credits

    def to_dict(self):
        return {
            "name": self.name,
            "trimester": self.trimester,
            "credits": self.credits
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['trimester'], data['credits'])

class GradeBook:
    def __init__(self):
        self.student_list = []
        self.course_list = []

    def load_data(self):
        if os.path.exists('students.json'):
            with open('students.json', 'r') as f:
                self.student_list = [Student.from_dict(data) for data in json.load(f)]
        if os.path.exists('courses.json'):
            with open('courses.json', 'r') as f:
                self.course_list = [Course.from_dict(data) for data in json.load(f)]

    def save_data(self):
        with open('students.json', 'w') as f:
            json.dump([student.to_dict() for student in self.student_list], f)
        with open('courses.json', 'w') as f:
            json.dump([course.to_dict() for course in self.course_list], f)

    def add_student(self, email, names):
        if not any(student.email == email for student in self.student_list):
            new_student = Student(email, names)
            self.student_list.append(new_student)
            self.save_data()
        else:
            print(f"Student with email {email} already exists.")

    def add_course(self, name, trimester, credits):
        if not any(course.name == name for course in self.course_list):
            new_course = Course(name, trimester, credits)
            self.course_list.append(new_course)
            self.save_data()
        else:
            print(f"Course with name {name} already exists.")

    def register_student_for_course(self, student_email, course_name, grade):
        student = next((s for s in self.student_list if s.email == student_email), None)
        course = next((c for c in self.course_list if c.name == course_name), None)
        if student and course:
            student.register_for_course(course, grade)
            self.save_data()
        else:
            print("Student or course not found.")

    def calculate_ranking(self):
        self.student_list.sort(key=lambda student: student.GPA, reverse=True)
        return [(student.email, student.GPA) for student in self.student_list]

    def search_by_grade(self, min_gpa, max_gpa):
        return [(student.email, student.GPA) for student in self.student_list if min_gpa <= student.GPA <= max_gpa]

    def generate_transcript(self, student_email):
        student = next((s for s in self.student_list if s.email == student_email), None)
        if student:
            return {
                "email": student.email,
                "names": student.names,
                "GPA": student.GPA,
                "courses": [{"name": course["course"].name, "grade": course["grade"]} for course in student.courses_registered]
            }

def main():
    gradebook = GradeBook()
    gradebook.load_data()

    while True:
        print("\nMenu:")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Register Student for Course")
        print("4. Calculate Ranking")
        print("5. Search by Grade")
        print("6. Generate Transcript")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            email = input("Enter student email: ")
            names = input("Enter student names: ")
            gradebook.add_student(email, names)
        elif choice == "2":
            name = input("Enter course name: ")
            trimester = input("Enter course trimester: ")
            credits = int(input("Enter course credits: "))
            gradebook.add_course(name, trimester, credits)
        elif choice == "3":
            student_email = input("Enter student email: ")
            course_name = input("Enter course name: ")
            try:
                grade = float(input("Enter grade: "))
                gradebook.register_student_for_course(student_email, course_name, grade)
            except ValueError:
                print("Invalid grade. Please enter a number.")
        elif choice == "4":
            ranking = gradebook.calculate_ranking()
            for rank, (email, gpa) in enumerate(ranking, start=1):
                print(f"{rank}. {email} - GPA: {gpa}")
        elif choice == "5":
            try:
                min_gpa = float(input("Enter minimum GPA: "))
                max_gpa = float(input("Enter maximum GPA: "))
                students = gradebook.search_by_grade(min_gpa, max_gpa)
                for email, gpa in students:
                    print(f"{email} - GPA: {gpa}")
            except ValueError:
                print("Invalid GPA range. Please enter numbers.")
        elif choice == "6":
            student_email = input("Enter student email: ")
            transcript = gradebook.generate_transcript(student_email)
            if transcript:
                print(f"Transcript for {transcript['email']} ({transcript['names']}):")
                print(f"GPA: {transcript['GPA']}")
                for course in transcript["courses"]:
                    print(f"Course: {course['name']} - Grade: {course['grade']}")
            else:
                print("Student not found.")
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
