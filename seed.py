from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Group, Teacher, Subject, Student, Grade

Faker.seed(0)

engine = create_engine('sqlite:///university.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Seed groups
groups = ['group1', 'group2', 'group3']
for group_name in groups:
    group = Group(group_name=group_name)
    session.add(group)

# Seed teachers
teachers = [Faker().first_name() + ' ' + Faker().last_name() for _ in range(5)]
for teacher_name in teachers:
    teacher = Teacher(fullname=teacher_name)
    session.add(teacher)

# Seed subjects
subjects = [
    "Algorithms",
    "Computer Networks",
    "Cybersecurity",
    "Python Programming Level II",
    "Relational Databases",
]
for subject_name in subjects:
    teacher_id = Faker().random_int(min=1, max=5)
    subject = Subject(name=subject_name, teacher_id=teacher_id)
    session.add(subject)

# Seed students
students = [
    (Faker().first_name() + ' ' + Faker().last_name(), Faker().random_int(min=1, max=len(groups)))
    for _ in range(40)
]
for student_data in students:
    student = Student(fullname=student_data[0], group_id=student_data[1])
    session.add(student)

# Seed grades
for student_id in range(1, 41):
    for subject_id in range(1, 6):
        grade = Faker().random_int(min=1, max=12)
        grade_date = Faker().date_between(start_date='-1y', end_date='today')
        grade_entry = Grade(subject_id=subject_id, student_id=student_id, grade=grade, grade_date=grade_date)
        session.add(grade_entry)

session.commit()
