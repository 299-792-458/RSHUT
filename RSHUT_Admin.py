import socket
import os
import threading
import time

def command_help():
    print('''
    Для выключения компьютера введите его IP, название или номер, 
    а затем используйте аргументы s для выключения, r для перезагрузки или m
    для отправки сообщения. Отсутствие аргумента равносильно аргументу s.
    Одно любое слово, указанное после адреса, будет отправлено как сообщение.
    Для отправки более длинных сообщений используйте аргумент m.
    Для выключения всех компьютеров введите All
    Для очистки поля выводы введите Clear.
    
    [s] - shutdown - выключение
    [r] - reboot   - перезагрузка
    [m] - message  - сообщение
 
    В файле config.txt вы можете дать компьютерам свое короткое новое имя
    и поставив пробел указать адрес. Каждая новая пара имени и адреса
    должны быть на новой строке.
    Обратиться к ним теперь можно будет по указанному вами имени.
    
    Важно: Избегайте пустых строк!
    
    Пример: 
        Имя_1 IP-адрес_1 
        Имя_2 IP-адрес_2
        ...
        Имя_N IP-адрес_N 
 
    Примеры: 
        192.168.2.27 s - выключение компьютера с указанным адресом
        INF-1 r        - перезагрузка компьютера с указанным сетевым именем
        1 m            - отправка длинного сообшения компьютеру под номером 1
        5              - выключение компьютера под номером 5
        INF-7 text     - отправка короткого сообщения 'text'
        all            - выключение всех компьютеров
        ALL s          - выключение всех компьютеров
        All R          - перезагрузка всех компьютеров
        aLl m          - отправка сообщения всем компьютерам
        clear          - очистить вывод
        
        
    DAVID_AG 25.02.24 v1.6
    
    ''')

def start():
    os.system('color c')
    print('RSHUT v1.6\nНапишите Help для вызова подсказки\n')

    while True:
        global msg
        # Создание курсора
        print('\n>> ', end='')
        # Чтение адресов из конфиг файла
        ip_dict = {}
        try:
            config = open('config.txt', 'r', encoding='utf-8')
            for line in config:
                key = line.split()[0]
                item = line.split()[1]
                ip_dict[key] = item
            config.close()
        except FileNotFoundError:
            # Создание конфиг файла, если такого файла изначально нет
            config = open('config.txt', 'x', encoding='utf-8')
            config.close()
        except (IndexError, KeyError, ValueError):
            print('\n<!> Файл config.txt заполнен неверно! Напишите Help для подсказки.')
            print(ip_dict)

        # Функция разбития цикла на потоки для работы со 'все'
        def command_for_all(argument):
            threads = []
            for value in ip_dict.values():
                thread = threading.Thread(target=client, args=(value, argument, ))
                threads.append(thread)

            for thread in threads:
                time.sleep(0.05)
                thread.start()

            for thread in threads:
                thread.join()

        # Ввод данных пользователем
        # [адрес] [атрибут]
        input_data = input().split()
        # Выключение по умолчанию
        if len(input_data) == 1:
            input_data.append('s')

        if input_data[0] in ip_dict:
            input_data[0] = ip_dict[input_data[0]]

        # Выключить все
        if (input_data[0].lower() == 'all' or input_data[0].lower() == 'фдд' or input_data[0].lower() == 'все') and (input_data[1].lower() == 's' or input_data[1].lower() == 'ы'):
            command_for_all('s')

        # Перезагрузить все
        elif (input_data[0].lower() == 'all' or input_data[0].lower() == 'фдд' or input_data[0].lower() == 'все') and (input_data[1].lower() == 'r' or input_data[1].lower() == 'к'):
            command_for_all('r')

        # Сообщение всем
        elif (input_data[0].lower() == 'all' or input_data[0].lower() == 'фдд' or input_data[0].lower() == 'все') and (input_data[1].lower() == 'm' or input_data[1].lower() == 'ь'):
            msg = input('Введите сообщение для всех: ')
            command_for_all(msg)

        # Отправить длинное сообщение
        elif input_data[1].lower() == 'm' or input_data[1].lower() == 'ь':
            msg = input('Введите сообщение: ')
            client(input_data[0], msg)

        # Вызвать Help
        elif input_data[0].lower() == 'help' or input_data[0].lower() == 'рудз' or input_data[0].lower() == 'помощь':
            command_help()

        elif input_data[0].lower() == 'clear' or input_data[0].lower() == 'сдуфк' or input_data[0].lower() == 'очистить':
            os.system('cls')
            print('RSHUT v1.6\nНапишите Help для вызова подсказки\n')

        # Выключить/перезагрузить/короткое сообщение по ip
        else:
            client(input_data[0], input_data[1])

def client_short(ip, port, argument):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #socket.setdefaulttimeout(5) # установить таймаут подключения
    client_socket.connect((str(ip), port))
    client_socket.send(argument.encode('utf-8'))
    data = client_socket.recv(1024)
    print(f"{data.decode('utf-8')}")
    client_socket.close()

def client1(ip, argument):
    try:
        client_short(ip, 9093, argument)
    except:
        print('\n<!> Невозможно подключиться к ', ip, ':9093', sep='')

def client2(ip, argument):
    try:
        client_short(ip, 9094, argument)
    except:
        print('\n<!> Невозможно подключиться к ', ip, ':9094', sep='')


def client(ip, argument):
    thread1 = threading.Thread(target=client1(ip, argument))
    thread1.start()

    thread2 = threading.Thread(target=client2(ip, argument))
    thread2.start()

if __name__ == "__main__":
    start()
