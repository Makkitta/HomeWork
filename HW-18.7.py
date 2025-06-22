import random
students = ['Александра', 'Аполон', 'Ярослав', 'Дарья', 'Ангелина', 'Илья', 'Кирилл']
students.sort()
classes = ['Литература', 'Обществознание', 'Русский язык']
students_marks = {}
for student in students:
    students_marks[student] = {}
    for class_ in classes:
        marks = [random.randint(1, 5) for i in range(3)]
        students_marks[student][class_] = marks
for student in students:
    print(f'''{student}
    {students_marks[student]}''')

print('''
Список команд:
1. Добавить оценки ученика по предмету.
2. Удалить оценку ученика по предмету.
3. Изменить оценку ученика по предмету.
4. Добавить нового ученика.
5. Удалить ученика.
6. Вывести средний балл по всем предметам по каждому ученику.
7. Вывести средний балл по всем предметам для выбранного ученика.
8. Вывести все оценки для выбранного ученика.
9. Вывести все оценки по всем ученикам.
10. Добавить новый предмет.
11. Удалить предмет.
12. Список предметов.
13. Список учеников.
14. Выход из программы.
''')
while True:
    command = int(input('Введите команду: '))
    if command == 1:
        print('1. Добавить оценку ученика по предмету')
        student = input('Введите имя ученика: ')
        class_ = input('Введите предмет: ')
        mark = int(input('Введите оценку: '))
        if student in students_marks.keys() and class_ in students_marks[student].keys():
            students_marks[student][class_].append(mark)
            print(f'Для ученика {student} по предмету {class_} добавлена оценка {mark}')
        else:
            print('ОШИБКА: неверное имя ученика или название предмета!')
    elif command == 2:
        print('2. Удалить оценку ученика по предмету.')
        student = input('Введите имя ученика: ')
        class_ = input('Введите предмет: ')
        mark = int(input('Введите оценку: '))
        if student in students_marks.keys() and class_ in students_marks[student].keys():
            students_marks[student][class_].remove(mark)
            print(f'Для ученика {student} по предмету {class_} удалена оценка {mark}')
        else:
            print('ОШИБКА: неверное имя ученика или название предмета!')
    elif command == 3:
        print('3. Изменить оценку ученика по предмету.')
        student = input('Введите имя ученика: ')
        class_ = input('Введите предмет: ')
        if student in students_marks and class_ in students_marks[student]:
            marks = students_marks[student][class_]
            marks.sort()
            print(f'Оценки: {marks}')
            old = int(input('Какую оценку изменить? '))
            new = int(input('Новая оценка: '))
            if old in marks:
                marks[marks.index(old)] = new
                marks.sort()
                print('Оценка успешно исправлена!')
            else:
                print('Оценка не найдена')
        else:
            print('ОШИБКА: неверное имя ученика или название предмета!')
    elif command == 4:
        print('4. Добавить нового ученика.')
        student = input('Введите имя нового ученика: ')
        students.append(student)
        students.sort()
        students_marks[student] = {}
        for class_ in classes:
            marks = [random.randint(1, 5) for i in range(3)]
            students_marks[student][class_] = marks
        print(f'''Новый ученик {student} добавлен в класс.
              Список всех учеников: {students}''')
    elif command == 5:
        print('5. Удалить ученика.')
        student = input('Введите имя ученика для удаления: ')
        if student in students:
            students.remove(student)
            students.sort()
            if student in students_marks:
                del students_marks[student]
                print(f'''Ученик {student} удалён из класса.
                              Список всех учеников: {students}''')
        else:
            print('ОШИБКА: Такого ученика нет в списке!')
    elif command == 6:
        print('6. Вывести средний балл по всем предметам каждого ученика')
        for student in students:
            print(student)
            for class_ in classes:
                marks_sum = sum(students_marks[student][class_])
                marks_count = len(students_marks[student][class_])
                print(f'{class_} - {marks_sum//marks_count}')
                print()
    elif command == 7:
        print('7. Вывести средний балл по всем предметам для выбранного ученика.')
        student = input('Введите имя ученика: ')
        if student in students_marks:
            print(f'Средний балл ученика {student}: ')
            for class_ in classes:
                marks_sum = sum(students_marks[student][class_])
                marks_count = len(students_marks[student][class_])
                print(f' {class_} - {marks_sum//marks_count}')
                print()
        else:
            print('ОШИБКА: Такого ученика нет в списке!')
    elif command == 8:
        print('8. Вывести все оценки для выбранного ученика.')
        student = input('Введите имя ученика: ')
        if student in students_marks:
            print(f'Список всех оценок ученика {student}: ')
            for class_ in classes:
                print(f' {class_} - {students_marks[student][class_]}')
        else:
            print('ОШИБКА: Такого ученика нет в списке!')
    elif command == 9:
        print('9. Вывести все оценки по всем ученикам')
        for student in students:
            print(student)
            for class_ in classes:
                print(f'\t{class_} - {students_marks[student][class_]}')
            print()
    elif command == 10:
        print('10. Добавить новый предмет.')
        class_ = input('Введите название нового предмета: ')
        if class_ not in classes:
            classes.append(class_)
            for student in students:
                students_marks[student][class_] = []
            print(f'Новый предмет {class_} успешно добавлен!')
        else:
            print('ОШИБКА: Такой предмет уже есть в списке!')
            print()
    elif command == 11:
        print('11. Удалить предмет.')
        class_ = input('Введите название предмета: ')
        if class_ in classes:
            classes.remove(class_)
            for student in students:
                del students_marks[student][class_]
            print(f'Предмет {class_} успешно удалён!')
        else:
            print('ОШИБКА: Такого предмета нет в списке!')
            print()
    elif command == 12:
        print('12. Список предметов.')
        print('Предметы: ')
        for class_ in classes:
            print(f'\t{class_} ')
    elif command == 13:
        print('13. Список учеников.')
        print('Ученики: ')
        for student in students:
            print(f'\t{student} ')
    elif command == 14:
        print('14. Выход из программы.')
        print('До свидания!')
        break

