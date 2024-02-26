import socket
import os
import tkinter as tk

# функция показа сообщения
def show_message(msg):
    window = tk.Tk()

    window.geometry("700x300")
    center_x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2  # вычислить координату X для центрирования
    center_y = (window.winfo_screenheight() - window.winfo_reqheight()) / 2  # вычислить координату Y для центрирования
    window.wm_geometry("+%d+%d" % ((center_x - 255), (center_y - 65)))  # задать позицию окна по центру

    window.title("Сообщение от Администратора")
    window.attributes('-topmost', True)
    frame = tk.Frame(window, bg="#E53935", bd=5, padx=10, pady=10)
    frame.pack(fill='x')
    label = tk.Label(frame, text=msg, font=("Roboto", 35), fg="#131418", bg="#E53935")
    label.pack(pady=40)
    button = tk.Button(window, text="МНЕ ПОНЯТНО", command=window.destroy, font=("Roboto", 12), width=22, height=10, relief=tk.FLAT, fg="#131418", bg="#CFD8DC")
    button.pack(pady=40)
    window.mainloop()

def start_server():
    # получение ip адреса на текущей машине
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    # попытка создания сервера на порте 9093
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((s.getsockname()[0], 9093))
        print(s.getsockname()[0] + ':9093')
        s.close()
        server_socket.listen(1)
    except: # попытка создания сервера на порте 9094
        try:
            server_socket.bind((s.getsockname()[0], 9094))
            print(s.getsockname()[0] + ':9094')
            s.close()
            server_socket.listen(1)
        except:
            pass

    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024).decode('utf-8')
        if data == 's':
            os.system("shutdown /s /t 0")
            client_socket.send("ОТВЕТ: Идёт выключение".encode('utf-8'))
        elif data == 'r':
            os.system("shutdown /r /t 0")
            client_socket.send("ОТВЕТ: Идёт перезагрузка".encode('utf-8'))
        else:
            try:
                client_socket.send("ОТВЕТ: Сообщение доставлено".encode('utf-8'))
                show_message(data)
            except:
                pass
        client_socket.close()

if __name__ == "__main__":
    start_server()