from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Group, Teacher, Subject, Student, Grade
import random

engine = create_engine('sqlite:///university.sqlite')
Session = sessionmaker(bind=engine)
session = Session()


def select_1():
    '''Task 1: Знайти 5 студентів із найбільшим середнім балом з усіх предметів.'''
    result = session.query(Student, func.avg(Grade.grade).label('avg_grade')) \
        .join(Grade).group_by(Student).order_by(func.avg(Grade.grade).desc()).limit(5).all()
    return result


def select_2(subject_name):
    '''Task 2: Знайти студента із найвищим середнім балом з певного предмета.'''
    result = session.query(Student, func.avg(Grade.grade).label('avg_grade')) \
        .join(Grade).join(Subject).filter(Subject.name == subject_name) \
        .group_by(Student).order_by(func.avg(Grade.grade).desc()).first()
    return result


def select_3(subject_name):
    '''Task 3: Знайти середній бал у групах з певного предмета.'''
    return (
        session.query(Group.group_name, func.avg(
            Grade.grade).label('avg_grade'))
        .join(Student, Group.students)
        .join(Grade, Student.grades)
        .join(Subject, Grade.subject)
        .filter(Subject.name == subject_name)
        .group_by(Group.group_name)
        .all()
    )


def select_4():
    '''Task 4: Знайти середній бал на потоці (по всій таблиці оцінок).'''
    result = session.query(func.avg(Grade.grade))
    return result[0]


def select_5():
    '''Task 5: Знайти які курси читає певний викладач.'''
    teacher = random.choice(session.query(Teacher).all())
    result = session.query(Subject.name).join(Teacher).filter(
        Teacher.fullname == teacher.fullname).all()
    return result


def select_6(group_name):
    '''Task 6: Знайти список студентів у певній групі.'''
    result = session.query(Student.fullname).join(
        Group).filter(Group.group_name == group_name).all()
    return result


def select_7(group_name, subject_name):
    '''Task 7: Знайти оцінки студентів у окремій групі з певного предмета.'''
    result = session.query(Student.fullname, Grade.grade) \
        .join(Group).join(Grade).join(Subject).filter(Group.group_name == group_name, Subject.name == subject_name).all()
    return result


def select_8():
    '''Task 8: Знайти середній бал, який ставить певний викладач зі своїх предметів.'''
    teacher = random.choice(session.query(Teacher).all())
    result = session.query(func.avg(Grade.grade).label('avg_grade')) \
        .join(Subject).join(Teacher).filter(Teacher.fullname == teacher.fullname).first()
    return result[0]


def select_9():
    '''Task 9: Знайти список курсів, які відвідує певний студент.'''
    student = random.choice(session.query(Student).all())
    result = (
        session.query(Subject.name)
        .select_from(Student)
        .join(Grade)
        .join(Subject)
        .filter(Student.fullname == student.fullname)
        .all()
    )
    return result


def select_10():
    '''Task 10: Список курсів, які певному студенту читає певний викладач.'''
    student = random.choice(session.query(Student).all())
    teacher = random.choice(session.query(Teacher).all())
    result = session.query(Subject.name) \
        .join(Teacher).join(Grade).join(Student).filter(Student.fullname == student.fullname, Teacher.fullname == teacher.fullname).all()
    return result


if __name__ == "__main__":
    result_select_1 = select_1()
    print("\nSelect 1 Result:")
    for student, avg_grade in result_select_1:
        print(f"{student.fullname}: {avg_grade:.2f}")

    result_select_2 = select_2("Algorithms")
    print("\nSelect 2 Result:")
    print(f"{result_select_2[0].fullname}: {result_select_2[1]:.2f}")

    result_select_3 = select_3("Algorithms")
    print("\nSelect 3 Result:")
    for group_name, avg_grade in result_select_3:
        print(f"{group_name}: {avg_grade:.2f}")

    result_select_4 = select_4()
    print("\nSelect 4 Result:")
    print(f"Average Grade: {avg_grade:.2f}")

    result_select_5 = select_5()
    print("\nSelect 5 Result:")
    print(result_select_5)

    result_select_6 = select_6("group1")
    print("\nSelect 6 Result:")
    print(result_select_6)

    result_select_7 = select_7("group1", "Algorithms")
    print("\nSelect 7 Result:")
    print(result_select_7)

    result_select_8 = select_8()
    print("\nSelect 8 Result:")
    print(result_select_8)

    result_select_9 = select_9()
    print("\nSelect 9 Result:")
    print(result_select_9)

    result_select_10 = select_10()
    print("\nSelect 10 Result:")
    print(result_select_10)
