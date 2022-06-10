from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout,
QVBoxLayout, QFormLayout)

app = QApplication([])
notes = []

'''Интерфейс приложения'''
#параметры окна
notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')#название окна
notes_win.resize(900, 600)#делаем размер окна

#виджеты окна приложения
list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')#список заметок

button_note_create = QPushButton('Создать заметку')#появляется окно с полем "Введите заметки"
button_note_del = QPushButton('Удалите заметку')#появляется окно с полем Удалите заметку
button_note_save = QPushButton('Сохранить заметку')#появляется окно с полем Сохранить заметку

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')#появляется надпись Введите тег
field_text = QTextEdit()
button_tag_add = QPushButton('Добавить к заметке')#появляется надпись Добавить к заметке
button_tag_del =QPushButton('Открепить от заметки')#появляется надпись Открепить от заметки
button_tag_search = QPushButton('Искатьзаметки по тегу')#появляется надпись Искатьзаметки по тегу
list_tags = QListWidget()#создаем виджет
list_tags_label = QLabel('Список тегов')#появляется надпись Список тегов

#расположениевиджетов по лэйаутам
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()#создаем лэйауты с окном заметок
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1 = QHBoxLayout()#создаем лэйаут сщздать и удалить заметку
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
row_2 =QHBoxLayout()#создаем лэйаут сохранить заметку
row_2.addWidget(button_note_save)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)#сооздаем виджет с надписью теги
col_2.addWidget(list_tags_label)
col_2.addWidget(field_tag)
row_3 = QHBoxLayout()#создаем лэйаут для кнопки сохранить и удалить тег
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
row_4 = QHBoxLayout()#создаем лэйаут для кнопки найти тег
row_4.addWidget(button_tag_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)

'''Функционал приложения'''
def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    for note in notes:
        if note[0] == key:
            field_text.setText(note[1])
            list_tags.clear()
            list_tags.addItems(note[2])

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Добавить заметку", "Название заметки")
    if ok and note_name != "":
        note = list()
        note = [note_name, '', []]
        notes.append(note)
        list_notes.addItem(note[0])
        list_tags.addItem(note[2])
        print(notes)
        with open(str(len(note)-1)+"txt", "w") as file:
            file.write(note[0]+'\n')

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        index = 0
        for note in notes:
            if note[0] == key:
                note[1] = field_text.toPlainText()
                with open(str(index)+ "txt","w") as file:
                    file.write(note[0]+'\n')
                    file.write(note[1]+'\n')
                    for tag in note[2]:
                        file.write(tag+' ')
                    file.write('\n')
            index += 1
        print(notes)
    else:
        print("Заметки для сохранения не выбранна!")

#обработка событий
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)

#запуск приложения
notes_win.show()

name = 0
note = []
while True:
    filename = str(name)+".txt"
    try:
        with open(filename, "r")as file:
            for line in file:
                line = line.replace('\n', '')
                note.append(line)
        tags = note[2].split(' ')
        note[2] = tags

        notes.append(note)
        note = []
        name += 1

    except IOError:
        break

print(notes)
for note in notes:
    list_notes.addItem(note[0])

app.exec_()