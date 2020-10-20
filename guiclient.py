from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  
            break


def send(event=None): 
    msg = my_msg.get()
    my_msg.set("") 
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    my_msg.set("{quit}")
    send()


HOST = input('Enter host: ')
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

top = tkinter.Tk()
top.title("Chat Application")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH,expand=True)
msg_list.pack(fill=tkinter.BOTH,expand=True)
scrollbar.config( command = msg_list.yview )
messages_frame.pack(fill=tkinter.BOTH,expand=True)

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack(fill=tkinter.BOTH,expand=True)
send_button = tkinter.Button(top, text="Send", command=send, bg='#33c028')
send_button.pack(fill=tkinter.BOTH,expand=True)

top.protocol("WM_DELETE_WINDOW", on_closing)



client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop() 
