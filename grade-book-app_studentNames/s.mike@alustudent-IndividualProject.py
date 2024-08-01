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
            points = self.grade_to_points(grade) * course.credits
            total_points += points
            total_credits += course.credits

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
        self.courses_registered.append((course, grade))
        

class Course:
    def __init__(self, name, trimester, credits):
        self.name = name
        self.trimester = trimester
        self.credits = credits


class GradeBook:
    def __init__(self):
        self.student_list = []
        self.course_list = []

    def add_student(self, email, names):
        student = Student(email, names)
        self.student_list.append(student)
        print(f"Student {names} added.")

    def add_course(self, name, trimester, credits):
        course = Course(name, trimester, credits)
        self.course_list.append(course)
        print(f"Course {name} added.")

    def register_student_for_course(self, email, course_name, grade):
        student = self.find_student_by_email(email)
        course = self.find_course_by_name(course_name)
        if student and course:
            student.register_for_course(course, grade)
            print(f"Student {student.names} registered for course {course.name} with grade {grade}.")
        else:
            print("Student or course not found.")

    def calculate_GPA(self, email):
        student = self.find_student_by_email(email)
        if student:
            gpa = student.calculate_GPA()
            print(f"GPA for {student.names} is {gpa:.2f}.")
        else:
            print("Student not found.")

    def calculate_ranking(self):
        self.student_list.sort(key=lambda student: student.GPA, reverse=True)
        for rank, student in enumerate(self.student_list, start=1):
            print(f"Rank {rank}: {student.names} with GPA {student.GPA:.2f}")

    def search_by_grade(self, grade):
        result = []
        for student in self.student_list:
            for course, course_grade in student.courses_registered:
                if course_grade == grade:
                    result.append((student, course))
        
        for student, course in result:
            print(f"Student {student.names} got grade {grade} in {course.name}.")

    def generate_transcript(self, email):
        student = self.find_student_by_email(email)
        if student:
            print(f"Transcript for {student.names}:")
            for course, grade in student.courses_registered:
                print(f"Course: {course.name}, Trimester: {course.trimester}, Credits: {course.credits}, Grade: {grade}")
            print(f"Overall GPA: {student.GPA:.2f}")
        else:
            print("Student not found.")

    def find_student_by_email(self, email):
        for student in self.student_list:
            if student.email == email:
                return student
        return None

    def find_course_by_name(self, name):
        for course in self.course_list:
            if course.name == name:
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
