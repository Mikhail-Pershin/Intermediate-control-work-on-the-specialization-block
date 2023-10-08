"""""
В приведенном примере все заметки сохраняются в файл "notes.csv", 
а при запуске приложения они загружаются из этого файла. 
Команды "add", "edit" и "delete" выполняют операции по добавлению, редактированию и удалению заметок соответственно. 
Команда "print" выводит все заметки на экран. 
Команда "filter" позволяет отфильтровать заметки по дате. 
Команда "exit" завершает выполнение приложения.

Вызов данного скрипта без параметров запустит интерактивный режим работы с заметками через командную строку.
"""""

import csv
import datetime


#  класс Note, который будет представлять отдельную заметку

class Note:
    def __init__(self, note_id, title, message, datetime_created, datetime_modified):
        self.note_id = note_id
        self.title = title
        self.message = message
        self.datetime_created = datetime_created
        self.datetime_modified = datetime_modified

#  класс NoteApp, который будет выполнять операции по сохранению, чтению, добавлению, редактированию и удалению заметок.

class NoteApp:
    def __init__(self):
        self.notes = []

    def save_notes_to_csv(self):
        with open('notes.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for note in self.notes:
                writer.writerow([note.note_id, note.title, note.message, note.datetime_created, note.datetime_modified])

    def load_notes_from_csv(self):
        try:
            with open('notes.csv', 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                for row in reader:
                    note_id, title, message, datetime_created, datetime_modified = row
                    datetime_created = datetime.datetime.strptime(datetime_created, "%Y-%m-%d %H:%M:%S")
                    datetime_modified = datetime.datetime.strptime(datetime_modified, "%Y-%m-%d %H:%M:%S")
                    note = Note(note_id, title, message, datetime_created, datetime_modified)
                    self.notes.append(note)
        except FileNotFoundError:
            pass

    def add_note(self, title, message):
        note_id = len(self.notes) + 1
        datetime_now = datetime.datetime.now()
        note = Note(note_id, title, message, datetime_now, datetime_now)
        self.notes.append(note)
        self.save_notes_to_csv()

    def delete_note(self, note_id):
        self.notes = [note for note in self.notes if note.note_id != note_id]
        self.save_notes_to_csv()

    def edit_note(self, note_id, new_title, new_message):
        for note in self.notes:
            if note.note_id == note_id:
                note.title = new_title
                note.message = new_message
                note.datetime_modified = datetime.datetime.now()
        self.save_notes_to_csv()

    def print_notes(self):
        for note in self.notes:
            print(f"ID: {note.note_id}")
            print(f"Title: {note.title}")
            print(f"Message: {note.message}")
            print(f"Created: {note.datetime_created}")
            print(f"Modified: {note.datetime_modified}")
            print()

    def filter_notes_by_date(self, date):
        filtered_notes = [note for note in self.notes if note.datetime_created.date() == date]
        return filtered_notes

# Пример использования NoteApp

note_app = NoteApp()
note_app.load_notes_from_csv()

while True:
    command = input("Введите команду (add, edit, delete, print, filter, exit): ")

    if command == "add":
        title = input("Введите заголовок заметки: ")
        message = input("Введите тело заметки: ")
        note_app.add_note(title, message)
        print("Заметка успешно сохранена")

    elif command == "edit":
        note_id = int(input("Введите ID заметки для редактирования: "))
        new_title = input("Введите новый заголовок заметки: ")
        new_message = input("Введите новое тело заметки: ")
        note_app.edit_note(note_id, new_title, new_message)
        print("Заметка успешно отредактирована")

    elif command == "delete":
        note_id = int(input("Введите ID заметки для удаления: "))
        note_app.delete_note(note_id)
        print("Заметка успешно удалена")

    elif command == "print":
        note_app.print_notes()

    elif command == "filter":
        date_str = input("Введите дату фильтрации в формате ГГГГ-ММ-ДД: ")
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        filtered_notes = note_app.filter_notes_by_date(date)
        for note in filtered_notes:
            print(f"ID: {note.note_id}")
            print(f"Title: {note.title}")
            print(f"Message: {note.message}")
            print(f"Created: {note.datetime_created}")
            print(f"Modified: {note.datetime_modified}")
            print()

    elif command == "exit":
        break