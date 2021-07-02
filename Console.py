import threading, sys, os, json
from backend import Client

if(os.path.isfile("setting.json")):
    load_settings = input("Load settings? (Y/n) ")
    load_settings = True if load_settings.lower() == "y" or not(load_settings) else False

if(load_settings):
    setting  = json.load(open("setting.json"))
    ip       = setting["ip"]
    port     = setting["port"]
    nickname = setting["nickname"]
    password = setting["password"]
    del(setting)
else:
    ip       = input("Enter ip: ") # Полечение IP
    port     = input("Enter port(enter to default): ") # Получение порта
    port     = int(port) if port.strip() else 2026 # Если порт пропущен, то стандартный
    nickname = input("Enter nickname: ") # Получение никнейма
    password = input("Enter password: ") # Получение пароля
    setting  = {
        "ip":ip,
        "port": port,
        "nickname": nickname,
        "password": password
    }
    f = open("setting.json", "w")
    json.dump(setting, f)
    f.close()
    del(setting, f)

class Main:
    commands = {
        "change_chat": [
            "chchat",
            "change_chat"
        ]
    }
    def __init__(self, ip, port, nickname, password):
        self.run = True
        self.chat = "#main"
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
            messages = self.internal_server.read_messages()
            if(messages is not None):
                for msg in messages:
                    nickname = msg['nickname']
                    message  = msg['message']
                    chat     = msg['chat']
                    print(f"[{chat}|{nickname}]: {message}")

    def parse_inp(self):
        while self.run:
            try:
                inp = input("")
            except KeyboardInterrupt:
                self.internal_server.disconnect()
                sys.exit()
            if(inp[0] == "/"):
                self.pars_commands(inp)
            else:
                self.internal_server.write_message(inp, self.chat)


    def pars_commands(self, command):
        command = command[1::]
        command = command.split(" ")
        if(command[0] in self.commands["change_chat"]):
            try:
                self.chat = command[1]
            except IndexError:
                print(f"ERROR: You need to set chat, like: /{command[0]} #main")
            else:
                print(f"Chat was changed to {command[1]}")
        else:
            print(f"Unknown command: /{command[0]}")

app = Main(ip, port, nickname, password)
