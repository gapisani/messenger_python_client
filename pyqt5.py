from PyQt5 import QtWidgets
from form import Ui_MainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from backend import Client
import sys, threading, os, json, platform
from PyQt5.QtCore import Qt
from datetime import datetime
# Импортируем все модули

# TODO: Сделать уведомления
# TODO: сделать панель с эмодзи
# TODO: Сделать картинки

# Класс для получения сообщений.
class Read(QThread):
    return_msg = pyqtSignal(dict)
    def run(self):
        while 1:
            try: internal_server
            except: continue
            if(internal_server.connect_):
                text_list = internal_server.read_messages() # Читаем сообщение
                if(text_list is not None):
                    for i in text_list:
                        self.return_msg.emit(i) # Возвращение сообщения

# Освновной класс.
class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()

        # Создание главного окна.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # При запуске текущий чат это #main
        self.current_chat = "#main"
        self.ui.chat_list.setCurrentItem(self.ui.chat_list.item(0))

        # Сообщения из чатов
        self.chat_messages = {}

        # Выключение возможности писать в поле для ввода сообщений и нажатия на кнопку "Send"
        self.ui.message.setReadOnly(True)
        self.ui.send_button.setEnabled(False)

        for i in range(self.ui.chat_list.count()):
            self.chat_messages[self.ui.chat_list.item(i).text()] = []

        # Попытка загрузить настройки
        try:
            with open("setting.json", "r") as rs:
                temp_st = json.load(rs)
            self.ui.ip.setText(temp_st["ip"])
            self.ui.port.setValue(temp_st["port"])
            self.ui.nickname.setText(temp_st["nickname"])
            self.ui.password.setText(temp_st["password"])
        except: pass

        # Подключение кнопок к функциям
        self.ui.send_button.clicked.connect(self.sendMessage) # Фулнкция sendMessage -> кнопка Send
        self.ui.connect_button.clicked.connect(self.connect) # Функция connect -> кнопка connect
        self.ui.chat_list.itemClicked.connect(self.changeChat) # Функция changeChat -> меню с чатами
        self.ui.add_chat_button.clicked.connect(self.add_chat)

    def connect(self): # Подключение
        global internal_server # Обявление сервера глобальным
        ip = self.ui.ip.text() # Получение ip
        port = self.ui.port.value() # Получение порта
        nickname = self.ui.nickname.text() # Получения никнейма
        password = self.ui.password.text() # Получение пароля

        # Загрузка настроек
        with open("setting.json", "w") as ws:
            json.dump({
                        "ip": ip,
                        "port": port,
                        "nickname": nickname,
                        "password": password,
                        "chat_list": list(self.chat_messages)
                    }, ws)


        try: # Если уже подключен, то отключаемся
            if(internal_server.connect_):
                internal_server.disconnect()
        except: # Если еще не был подключен
            internal_server = Client(ip, port, nickname, password) # Подключение бекенда

        try:
            self.msg_get = Read() # Запуск отдельного потока для чтения новых сообщений
            self.msg_get.return_msg.connect(self.onMessageGetted) # Подключение функции
            self.msg_get.start() # Запуск потока
        except: pass

        # Указание для бекенда никнейма, ip, порта и пароля
        internal_server.nickname = nickname
        internal_server.ip = ip
        internal_server.port = port
        internal_server.password = password

        self.ui.message.setReadOnly(False) # Включение поля ввода сообщений
        self.ui.send_button.setEnabled(True) # Включение кнопки
        internal_server.connect() # Подключение

    def changeChat(self, chat):
        if(chat.text() not in self.chat_messages):
            self.chat_messages[chat.text()] = []
        self.current_chat = chat.text()
        self.ui.chat.setText("")
        for i in self.chat_messages[self.current_chat]:
            self.ui.chat.append(i)

    def add_chat(self):
        self.ui.chat_list.addItem(self.ui.add_chat_name.text())
        try:
            with open("setting.json", "r") as rs:
                temp_st = json.load(rs)
            with open("setting.json", "w") as ws:
                json.dump({
                            "ip": temp_st["ip"],
                            "port": temp_st["port"],
                            "nickname": temp_st["nickname"],
                            "password": temp_st["password"],
                            "chat_list": list(self.chat_messages)
                        }, ws
                    )
        except Exception as e: print(e)
        self.ui.add_chat_name.setText("")

    def sendMessage(self): # Функция отправки сообщений
        msg = self.ui.message.text() # Получение текста из поля ввода
        self.ui.message.setText("") # Стереть текст в поле ввода
        internal_server.write_message(msg, self.current_chat) # Отправка сообщения

    def onMessageGetted(self, value): # Функция которая вызывается при новом сообщении
        try:
            self.chat_messages[value["chat"]].append(f"[{value['nickname']}]: {value['message']}")
        except KeyError:
            self.chat_messages[value["chat"]] = []
        if(self.current_chat in self.chat_messages):
            self.ui.chat.setText("")
            for i in self.chat_messages[self.current_chat]:
                self.ui.chat.append(i)
        else:
            value["chat"] = []
        if(platform.system() == "Linux" and self.isHidden()): # Если ОС с ядром Linux
            os.system(f"notify-send -a Messenger \"{value}\"") # То показываем уведомление

    def keyPressEvent(self, e): # Эвент на нажатие клавиши на клавиатуре
        if e.key() == Qt.Key_Return: # Если это ентер
            self.sendMessage() # Отправляем сообщение
        if e.key() == Qt.Key_Escape:
            sys.exit()


app = QtWidgets.QApplication([]) # Запуск приложения
application = mywindow()
application.show()

app.exec()

try: internal_server.disconnect() # Отключаемся при закрытии приложения
except NameError: pass
