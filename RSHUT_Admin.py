import socket
import os
import threading
import time
import tkinter as tk
from PIL import ImageTk

version = ['v1.9', '18.03.24']
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
        
                (\___/)
                (='.'=)
                (")_(")
       
    DAVID_AG {version[1]} {version[0]}
    ''')

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

def main_window():
    window = tk.Tk()
    center_x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2  # вычислить координату X для центрирования
    center_y = (window.winfo_screenheight() - window.winfo_reqheight()) / 2  # вычислить координату Y для центрирования
    window.wm_geometry("+%d+%d" % ((center_x - 410), (center_y - 365)))  # задать позицию окна по центру

    window.title("RSHUT " + version[0])

    img_shutdown = ImageTk.PhotoImage(file='icons/shutdown.ico')
    img_reboot = ImageTk.PhotoImage(file='icons/reboot.ico')
    img_message = ImageTk.PhotoImage(file='icons/message.ico')
    img_timer = ImageTk.PhotoImage(file='icons/timer.ico')
    img_timer_set = ImageTk.PhotoImage(file='icons/alarm_on.ico')
    img_timer_unset = ImageTk.PhotoImage(file='icons/alarm_off.ico')

    color_1 = "#CFD8DC"
    color_2 = "#F5F5F5"
    color_3 = "#131418"
    color_4 = "#E53935"
    i = 0

    def message_window(address):
        window = tk.Tk()
        window.geometry("400x300")
        window.title("ОТПРАВКА СООБЩЕНИЯ")

        edit = tk.Entry(window, width=50)
        edit.grid(row=1, column= 1, pady=[30, 0], padx=50)

        button = tk.Button(window, text="ОТПРАВИТЬ",
                           command= lambda: [client(ip_dict[address], edit.get()), window.destroy()],
                           font=("Roboto", 12), width=15, height=3,
                           relief=tk.FLAT, fg=color_3, bg=color_1)
        button.grid(row=2, column= 1, pady=[30, 0])

        window.mainloop()

    def timer_window(address):
        window = tk.Tk()
        window.geometry("400x300")
        window.title("ТАЙМЕР")

        edit = tk.Entry(window, width=50)
        edit.grid(row=1, column=1, pady=[30, 0], padx=50)

        button_set = tk.Button(window, text="ЗАДАТЬ",
                           command=lambda: [client(ip_dict[address], 's', timer=(edit.get())), window.destroy()],
                           font=("Roboto", 12), width=15, height=3,
                           relief=tk.FLAT, fg=color_3, bg=color_1)
        button_set.grid(row=2, column=1, pady=[30, 30])

        button_unset = tk.Button(window, text="ОТМЕНИТЬ",
                           command=lambda: [client(ip_dict[address], 'a'), window.destroy()],
                           font=("Roboto", 12), width=15, height=3,
                           relief=tk.FLAT, fg=color_3, bg=color_1)
        button_unset.grid(row=3, column=1, pady=[30, 0])

        window.mainloop()

    for address in ip_dict:
        if i%2 == 0:
            color_a = color_1
            color_b = color_2
        else:
            color_a = color_2
            color_b = color_1

        frame = tk.Frame(window, bg=color_a, bd=1, pady=20)
        frame.pack(fill='x')

        label = tk.Label(frame, text=address, font=("Roboto", 20), fg=color_3, bg=color_a)
        label.place(relx=0.02)

        button_shutdown = tk.Button(frame, text="ВЫКЛ.", image=img_shutdown,
                                    command=lambda address=address: client(ip_dict[address], 's', '0'),
                                    font=("Roboto", 12), width=100, height=100,
                                    relief=tk.FLAT, fg=color_3, bg=color_b)

        button_shutdown.grid(row=1, column= 1, padx=[250, 5])

        button_restart = tk.Button(frame, text="ПЕРЕЗ.", image=img_reboot,
                                   command=lambda address=address: client(ip_dict[address], 'r', '0'),
                                   font=("Roboto", 12), width=100, height=100,
                                   relief=tk.FLAT, fg=color_3, bg=color_b)

        button_restart.grid(row=1, column= 2, padx=[0, 5])

        button_msg = tk.Button(frame, text="СООБЩ.", image=img_message,
                                   command=lambda address=address: message_window(address),
                                   font=("Roboto", 12), width=100, height=100,
                                   relief=tk.FLAT, fg=color_3, bg=color_b)

        button_msg.grid(row=1, column=3, padx=[0, 5])

        button_timer = tk.Button(frame, text="ТАЙМ.", image=img_timer,
                                   command=lambda address=address: timer_window(address),
                                   font=("Roboto", 12), width=100, height=100,
                                   relief=tk.FLAT, fg=color_3, bg=color_b)

        button_timer.grid(row=1, column=4)

        i += 1

    frame_all = tk.Frame(window, bg=color_3, bd=1, pady=20, padx=300)
    frame_all.pack(fill='x')

    button_shutdown_all = tk.Button(frame_all, text="ВЫКЛ. ВСЕ", command=window.destroy, font=("Roboto", 12), width=8, height=1,
                                relief=tk.FLAT, fg=color_3, bg=color_2)
    button_shutdown_all.grid(row=1, column= 1, ipadx= 20, padx=10, pady=10)

    button_restart_all = tk.Button(frame_all, text="ПЕРЕЗ. ВСЕ", command=window.destroy, font=("Roboto", 12), width=8, height=1,
                               relief=tk.FLAT, fg=color_3, bg=color_2)
    button_restart_all.grid(row=2, column= 1, ipadx= 20)

    button_restart_all = tk.Button(frame_all, text="СООБЩ. ВСЕ", command=window.destroy, font=("Roboto", 12), width=8,
                                   height=1,
                                   relief=tk.FLAT, fg=color_3, bg=color_2)
    button_restart_all.grid(row=1, column=2, ipadx=20)

    button_restart_all = tk.Button(frame_all, text="ТАЙМ. ВСЕ", command=window.destroy, font=("Roboto", 12), width=8,
                                   height=1,
                                   relief=tk.FLAT, fg=color_3, bg=color_2)
    button_restart_all.grid(row=2, column=2, ipadx=20)


    window.mainloop()

msg = ''
def start():
    os.system('color c')
    print(f'RSHUT {version[0]}\nНапишите Help для вызова подсказки')

    while True:
        global msg
        # Создание курсора
        print('\n>> ', end='')

        # Функция разбития цикла на потоки для работы со 'все'
        def command_for_all(argument, timer='0'):
            threads = []
            for value in ip_dict.values():
                thread = threading.Thread(target=client, args=(value, argument, timer))
                threads.append(thread)

            for thread in threads:
                time.sleep(0.05)
                thread.start()

            for thread in threads:
                thread.join()

        # Ввод данных пользователем
        # [адрес] [атрибут] [время]
        input_data = input().split()

        if input_data == []:
            print('<‼> Вы ничего не ввели!')
            continue
        # Выключение по умолчанию
        if len(input_data) == 1:
            input_data.append('s')

        if input_data[0] in ip_dict:
            input_data[0] = ip_dict[input_data[0]]

        # Выключить все
        if (input_data[0].lower() == 'all' or input_data[0].lower() == 'фдд' or input_data[0].lower() == 'все') and (input_data[1].lower() == 's' or input_data[1].lower() == 'ы'):
            if len(input_data) == 2:
                input_data.append('0')
            command_for_all(input_data[1], input_data[2])

        # Перезагрузить все
        elif (input_data[0].lower() == 'all' or input_data[0].lower() == 'фдд' or input_data[0].lower() == 'все') and (input_data[1].lower() == 'r' or input_data[1].lower() == 'к'):
            if len(input_data) == 2:
                input_data.append('0')
            command_for_all(input_data[1], input_data[2])

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

def client(ip, argument, timer='0'):
    def client_port(ip, port, argument, timer):
        try:
            argument = argument + ' ' + timer
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((str(ip), port))
            client_socket.send(argument.encode('utf-8'))
            data = client_socket.recv(1024)
            print(f"{data.decode('utf-8')}")
            client_socket.close()
        except:
            print('\n<‼> Ощибка подключения к ', ip, ':',port, sep='')

    port = [9093, 9094]
    threading.Thread(target=client_port, args=(ip, port[0], argument, timer)).start()
    time.sleep(0.05)
    threading.Thread(target=client_port, args=(ip, port[1], argument, timer)).start()

if __name__ == "__main__":
    threading.Thread(target=start).start()
    threading.Thread(target=main_window).start()
