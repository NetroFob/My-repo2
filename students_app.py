import sqlite3

DB_NAME = 'students.db'


def init_db(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            group_name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            age INTEGER NOT NULL
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        initial_students = [
            ('Иванов Иван', 'ИСП-101', 5, 19),
            ('Петров Пётр', 'ИСП-101', 4, 18),
            ('Сидоров Алексей', 'ИСП-102', 3, 20),
            ('Смирнова Анна', 'ИСП-102', 5, 19),
            ('Кузнецов Максим', 'ИСП-101', 4, 18)
        ]
        cursor.executemany("INSERT INTO students (name, group_name, grade, age) VALUES (?, ?, ?, ?)", initial_students)
        conn.commit()
        print("База данных создана и заполнена начальными данными.\n")


def show_all_students(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    print("\n--- Список всех студентов ---")
    if not students:
        print("Студенты не найдены.")
    else:
        print(f"{'ID':<5} | {'ФИО':<25} | {'Группа':<10} | {'Оценка':<6} | {'Возраст'}")
        for s in students:
            print(f"{s[0]:<5} | {s[1]:<25} | {s[2]:<10} | {s[3]:<6} | {s[4]}")
    print()


def add_student(conn):
    print("\n--- Добавление студента ---")
    name = input("Введите ФИО студента: ")
    group_name = input("Введите название группы: ")

    while True:
        try:
            grade = int(input("Введите оценку (1-5): "))
            if 1 <= grade <= 5:
                break
            print("Оценка должна быть от 1 до 5.")
        except ValueError:
            print("Ошибка: введите целое число.")

    while True:
        try:
            age = int(input("Введите возраст студента: "))
            if age > 0:
                break
            print("Возраст должен быть больше 0.")
        except ValueError:
            print("Ошибка: введите целое число.")

    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, group_name, grade, age) VALUES (?, ?, ?, ?)",
                   (name, group_name, grade, age))
    conn.commit()
    print("Студент успешно добавлен!\n")


def search_by_group(conn):
    print("\n--- Поиск по группе ---")
    group_name = input("Введите название группы для поиска: ")
    cursor = conn.cursor()
    # Используем параметризованный запрос (?)
    cursor.execute("SELECT * FROM students WHERE group_name = ?", (group_name,))
    students = cursor.fetchall()

    print(f"\nСтуденты группы {group_name}:")
    if not students:
        print("Студенты в этой группе не найдены.")
    else:
        for s in students:
            print(f"ID: {s[0]} | ФИО: {s[1]} | Оценка: {s[3]}")
    print()


def search_by_grade(conn):
    print("\n--- Поиск по оценке ---")
    while True:
        try:
            grade = int(input("Введите оценку для поиска: "))
            break
        except ValueError:
            print("Ошибка: введите целое число.")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE grade = ?", (grade,))
    students = cursor.fetchall()

    print(f"\nСтуденты с оценкой {grade}:")
    if not students:
        print("Студенты с такой оценкой не найдены.")
    else:
        for s in students:
            print(f"ID: {s[0]} | ФИО: {s[1]} | Группа: {s[2]}")
    print()


def update_grade(conn):
    print("\n--- Изменение оценки ---")
    while True:
        try:
            student_id = int(input("Введите ID студента для изменения оценки: "))
            break
        except ValueError:
            print("Ошибка: введите целое число (ID).")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    if not cursor.fetchone():
        print(f"Студент с ID {student_id} не найден!\n")
        return

    while True:
        try:
            new_grade = int(input("Введите новую оценку (1-5): "))
            if 1 <= new_grade <= 5:
                break
            print("Оценка должна быть от 1 до 5.")
        except ValueError:
            print("Ошибка: введите целое число.")

    cursor.execute("UPDATE students SET grade = ? WHERE id = ?", (new_grade, student_id))
    conn.commit()
    print("Оценка успешно изменена!\n")


def delete_student(conn):
    print("\n--- Удаление студента ---")
    while True:
        try:
            student_id = int(input("Введите ID студента для удаления: "))
            break
        except ValueError:
            print("Ошибка: введите целое число (ID).")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    if not cursor.fetchone():
        print(f"Студент с ID {student_id} не найден!\n")
        return

    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    print("Студент успешно удален.")
    print("Оставшиеся студенты:")
    show_all_students(conn)


def show_average_grade(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(grade) FROM students")
    avg_grade = cursor.fetchone()[0]

    print("\n--- Средняя оценка ---")
    if avg_grade is not None:
        print(f"Средняя оценка всех студентов: {avg_grade:.2f}\n")
    else:
        print("База данных пуста, невозможно вычислить средний балл.\n")


def main():
    conn = sqlite3.connect(DB_NAME)

    try:
        init_db(conn)

        while True:
            print("===== УЧЁТ СТУДЕНТОВ =====")
            print("1. Показать всех студентов")
            print("2. Добавить студента")
            print("3. Найти студентов по группе")
            print("4. Найти студентов по оценке")
            print("5. Изменить оценку")
            print("6. Удалить студента")
            print("7. Показать средний балл")
            print("0. Выход")

            choice = input("Выберите пункт меню: ")

            if choice == '1':
                show_all_students(conn)
            elif choice == '2':
                add_student(conn)
            elif choice == '3':
                search_by_group(conn)
            elif choice == '4':
                search_by_grade(conn)
            elif choice == '5':
                update_grade(conn)
            elif choice == '6':
                delete_student(conn)
            elif choice == '7':
                show_average_grade(conn)
            elif choice == '0':
                print("Завершение работы программы. До свидания!")
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите пункт от 0 до 7.\n")

    finally:
        # Закрытие соединения после завершения программы
        conn.close()


if __name__ == "__main__":
    main()