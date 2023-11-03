from datetime import date
class User:
    objects = []
    def __init__(self, first_name: str, last_name: str, password: str):
        self.objects.append(self)
        self.first_name = first_name
        self.last_name = last_name
        self.__password = password
    def password_correct(self, password) -> bool:
        return self.__password == password
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
class Subject:
    objects = []
    def __init__(self, title: str, years: list[int]):
        self.objects.append(self)
        self.title = title
        self.years = years
    def __str__(self) -> str:
        return f"Subjet {self.title}"

class Teacher(User):
    objects = []
    def __init__(self, first_name: str, last_name: str, password: str, subjects: list[Subject]):
        self.objects.append(self)
        self.subjects = subjects
        super().__init__(first_name, last_name, password)

    def __str__(self) -> str:
        return f"Teacher {super().__str__()}" 


class Mark:
    objects = []
    def __init__(self, teacher: Teacher, subject: Subject, date: date, mark: int, comment: str|None=None):
        self.objects.append(self)
        self.subject = subject
        self.teacher = teacher
        self.date = date
        self.mark = mark
        self.comment = comment
    def __str__(self) -> str:
        answer = f"{self.mark} at {self.date}"
        if self.comment is not None:answer += f' with a comment "{self.comment}"'
        return answer
class Student(User):
    objects = []
    def __init__(self, first_name: str, last_name: str, password: str, year: int, letter: str):
        self.objects.append(self)
        self.letter = letter
        self.year = year
        self.diary = Diary(self)
        super().__init__(first_name, last_name, password)
    @property
    def grade(self) -> str:
        return f"{self.year}{self.letter}"
    def __str__(self) -> str:
        return f"Student {super().__str__()} {self.grade}"
    def get_marks(self, subject: Subject) -> list[Mark]:
        marks = []
        for mark in self.diary.marks:
            if mark.subject == subject:
                marks.append(mark)
        return marks
    def get_avr_mark(self, subject: Subject) -> float:
        marks = self.get_marks(subject)
        sum = 0
        for mark in marks:
            sum+=mark.mark
        return round(sum/len(marks), 2) if marks else -1
    def add_mark(self, subject: Subject, teacher: Teacher, mark: int, comment: str|None=None) -> Mark:
        self.diary.marks.append(Mark(teacher, subject, date.today(), mark, comment))
        return self.diary.marks[-1]
    def is_struggling(self, subject: Subject):
        return self.get_avr_mark(subject)<60

class Diary:
    objects = []
    def __init__(self, student: Student, marks: list[Mark] = None):
        self.objects.append(self)
        if marks is None: marks = []
        self.marks = marks
        self.student = student
    def __str__(self) -> str:
        return f"Diary of {self.student}"

sys = Subject("System engeneering", [3])
az = Teacher("Azimbaev", "D", "SecurePassword1*", [sys])
me = Student("Adil", "Akylov", "qwerty", 3, "B")
print(sys)
print(az)
print(me)
for mark in Mark.objects:
    print(mark)
me.add_mark(sys, az, 100, "Very good!")
for mark in Mark.objects:
    print(mark)
me.add_mark(sys, az, 30, "Acceptable")
for mark in Mark.objects:
    print(mark)
print(me.get_avr_mark(sys))
print(f"Struggling: {me.is_struggling(sys)}")
me.add_mark(sys, az, 0, "Bad")
for mark in Mark.objects:
    print(mark)
print(me.get_avr_mark(sys))
print(f"Struggling: {me.is_struggling(sys)}")

try:
    print(me.__password)
except AttributeError:
    pass