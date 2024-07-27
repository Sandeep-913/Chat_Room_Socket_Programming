import random
import socket
import threading
from threading import *


class Server:

    active_clients = []

    def listen_messages_from_clients(client, user_name):
        while 1:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                recd_msg = user_name + ' ~ ' + message
                Server.send_message_to_all(recd_msg)
            else:
                print("Message cannot be empty")
                exit(0)

    def send_message_to_all(message):
        for user in Server.active_clients:
            Server.send_message(user[1], message)

    def send_message(client, message):
        client.sendall(message.encode())

    def client_handler(client):
        while 1:
            user_name = client.recv(2048).decode('utf-8')
            if user_name != '':
                Server.active_clients.append((user_name, client))
                print(f"[{user_name} joined the room]\n")
                break
            else:
                print("Enter a valid username!!")
                exit(0)
        threading.Thread(target=Server.listen_messages_from_clients, args=(client, user_name)).start()

    def __init__(self):
        Choices = [301, 302, 303, 304, 305, 306, 307, 308, 309, 310]
        HOST = '127.0.0.1'
        PORT = random.choice(Choices)
        LIMIT = 5
        server = socket.socket()
        try:
            server.bind((HOST, PORT))
            print(f"Your room number is-{PORT}")
        except:
            print(f"Cannot bind to {HOST}-{PORT}")
        server.listen(LIMIT)
        pres_client = Client()
        while 1:
            client, address = server.accept()
            threading.Thread(target=Server.client_handler, args=(client,)).start()


class Client:

    def send_message_to_client(client):
        while 1:
            message = input("\nMessage: ")
            if message != '':
                client.sendall(message.encode())
            else:
                print("Message cannot be empty")


    def Listen_messages_from_server(client):
        while 1:
            response = client.recv(2048).decode('utf-8')
            if response!='':
                user_name = response.split(" ~ ")[0]
                content = response.split(" ~ ")[1]
                print(f"[{user_name}] ~ {content}")

    def Server_handler(client):
        user_name = input("Enter your name: \n")
        if user_name != '':
            client.sendall(user_name.encode())
        else:
            print("Invalid user name")
            exit(0)
        threading.Thread(target=Client.Listen_messages_from_server,args=(client,)).start()

        Client.send_message_to_client(client)

    def __init__(self):
        HOST = '127.0.0.1'
        PORT = int(input("Enter Room Number: "))
        client = socket.socket()
        try:
            client.connect((HOST, PORT))
            print("Joined room successfully")
        except:
            print("Unable to join the room")

        threading.Thread(target=Client.Server_handler, args=(client,)).start()


def user_input_func():
    print("Do You want to create a new room? - c")
    print("Do you want to join an existing room? - e")
    user_input = input()
    if user_input.lower() == 'c':
        server = Server()
    elif user_input.lower() == 'e':
        client = Client()
    else:
        print("Please enter a valid input")
        user_input_func()


def main():
    user_input_func()


if __name__ == '__main__':
    main()
