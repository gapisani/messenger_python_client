import threading, sys
from backend import Client


ip = input("Enter ip: ") # Полечение IP
port = input("Enter port(enter to default): ") # Получение порта
nickname = input("Enter nickname: ") # Получение никнейма
password = input("Enter password: ") # Получение пароля

if(port.replace(" ", "") == ""): port = 2026 # Если порт пропущен, то стандартный

class Main:
    def __init__(self, ip, port, nickname, password):
        self.run = True
        print("Configure internal server.")
        self.internal_server = Client(ip, port, nickname, password)
        print("Connect to server...")
        self.internal_server.connect()
        print("Successfully connect to server")
        self.read_thread = threading.Thread(target= self.print_messages) # Вывод сообщений
        self.read_thread.start()
        self.parse_inp()

    def print_messages(self):
        while self.run:
            print(self.internal_server.read_messages())

    def parse_inp(self):
        while self.run:
            inp = input("")
            if(inp == "/exit"):
                self.exit()
            else:
                self.internal_server.write_message(inp)


    def exit(self):
        self.run = False
        print("Press ctrl+c")
        sys.exit()


app = Main(ip, port, nickname, password)
