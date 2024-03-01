import socket
import os
import threading
import time

version = ['v1.7', '29.02.24']

def command_help():
    print(f'''
    <Í>
    
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
    [a] - abort    - сброс таймера
    
    Вы можете указать время, через которое произойдёт выключение/перезагрузка. Для этого через пробел
    укажите время в минутах.
 
    Командой config вы можете открыть файл конфигурации.
    В файле config.txt вы можете дать компьютерам свое короткое новое имя
    и через пробел указать адрес. Каждая новая пара имени и адреса
    должны быть на новой строке.
    Обратиться к ним теперь можно будет по указанному вами имени.
    Важно: Избегайте пустых строк!
    
    Пример заполнения файла config.txt: 
        Имя_1 IP-адрес_1 
        Имя_2 IP-адрес_2
        ...
        Имя_N IP-адрес_N 
 
    Примеры команд: 
        192.168.2.27 s - выключение компьютера с указанным адресом
        INF-1 r        - перезагрузка компьютера с указанным сетевым именем
        1 m            - отправка длинного сообшения компьютеру под номером 1
        5              - выключение компьютера под номером 5
        8.8.8.8 s 10   - выключение компьютера с указанным адресом через 10 минут
        8.8.8.8 a      - отменить выключение по таймеру
        INF-7 text     - отправка короткого сообщения 'text'
        all            - выключение всех компьютеров
        ALL s          - выключение всех компьютеров
        All R          - перезагрузка всех компьютеров
        aLl m          - отправка сообщения всем компьютерам
        clear          - очистить вывод
        config         - открыть файл конфигурации
        
    Для добавления программы в автозагрузку:
    WIN+R → shell:startup → скопируйте в открывшуюся папку файл RSHUT.EXE
        
       
    DAVID_AG {version[1]} {version[0]}
    ''')

def start():
    os.system('color c')
    print(f'RSHUT {version[0]}\nНапишите Help для вызова подсказки')

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
            command_for_all(input_data[1])
            if len(input_data) == 2:
                input_data.append('0')

        # Перезагрузить все
        elif (input_data[0].lower() == 'all' or input_data[0].lower() == 'фдд' or input_data[0].lower() == 'все') and (input_data[1].lower() == 'r' or input_data[1].lower() == 'к'):
            command_for_all(input_data[1])
            if len(input_data) == 2:
                input_data.append('0')

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

        # Очистить вывод
        elif input_data[0].lower() == 'clear' or input_data[0].lower() == 'сдуфк' or input_data[0].lower() == 'очистить':
            os.system('cls')
            print(f'RSHUT {version[0]}\nНапишите Help для вызова подсказки')

        # Открыть файл конфигурации
        elif input_data[0].lower() == 'config' or input_data[0].lower() == 'сщташп' or input_data[0].lower() == 'конфиг':
            try:
                threading.Thread(target=os.system, args=('config.txt', )).start()
                print('<Í> Открыт файл конфигурации')
            except:
                print('<‼> Файл конфигурации не найден')

        # Выключить/перезагрузить/короткое сообщение по ip
        else:
            if len(input_data) == 2:
                input_data.append('0')
            client(input_data[0], input_data[1], input_data[2])

def client_short(ip, port, argument):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #socket.setdefaulttimeout(5) # установить таймаут подключения
    client_socket.connect((str(ip), port))
    client_socket.send(argument.encode('utf-8'))
    data = client_socket.recv(1024)
    print(f"{data.decode('utf-8')}")
    client_socket.close()

def client1(ip, argument, timer):
    try:
        argument = argument + ' ' + timer
        client_short(ip, 9093, argument)
    except:
        print('\n<‼> Невозможно подключиться к ', ip, ':9093', sep='')

def client2(ip, argument, timer):
    try:
        argument = argument + ' ' + timer
        client_short(ip, 9094, argument)
    except:
        print('\n<‼> Невозможно подключиться к ', ip, ':9094', sep='')


def client(ip, argument, timer='0'):
    thread1 = threading.Thread(target=client1(ip, argument, timer))
    thread1.start()

    thread2 = threading.Thread(target=client2(ip, argument, timer))
    thread2.start()

if __name__ == "__main__":
    start()
