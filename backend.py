import socket, json, sys
# Импорт библиотек

class Client:
    def __init__(self, ip, port, nickname, password):
        self.server   = (ip, port) # Инициализация
        self.nickname = nickname
        self.password = password
        self.connect_ = False
        self.key      = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Создание сокета
        self.sock.bind(('', 0))
        self.sock.sendto( # Отправка сообщения о заходе
            json.dumps(
                {
                    "name": self.nickname,
                    "message": "",
                    "password": self.password,
                    "chat": "#main",
                    "chat_key": None,
                    "join": True,
                    "left": False
                }).encode('utf-8'),
            self.server)
        self.connect_ = True

    def disconnect(self):
        self.sock.sendto( # Отправка сообщения о выходе
            json.dumps(
                {
                    "name": self.nickname,
                    "message": "",
                    "chat": "#main",
                    "chat_key": None,
                    "password": self.password,
                    "join": False,
                    "left": True
                }).encode('utf-8'),
        self.server)
        self.connect_ = False

    def read_messages(self): # Чтение
        data = self.sock.recv(1048576)
        text = data.decode('utf-8')
        json_text = json.loads(text)
        return(json_text)

    def write_message(self, msg, chat="#main", chat_key=None): # Отправка сообщений
        if(self.connect_): # Если подключен
            if(msg.replace(" ", "") != ""): # Если сообщение не пустое
                self.sock.sendto( # Отправка сообщений
                    json.dumps(
                            {
                                "name": self.nickname,
                                "message": msg,
                                "chat": chat,
                                "chat_key": chat_key,
                                "password": self.password,
                                "join": False,
                                "left": False
                            }
                        ).encode('utf-8'),
                    self.server)
