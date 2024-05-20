import socket
import threading

name_id = {}
clients = []

def num_of_zero(len_name):
    if len_name > 10000:
        return "0" + str(len_name)
    elif len_name > 1000:
        return ("0" * 2) + str(len_name)  
    elif len_name > 100:
        return ("0" * 3) + str(len_name)  
    elif len_name > 10:
        return ("0" * 4) + str(len_name)
    else:
        return ("0" * 5) + str(len_name)

def is_name_unique(username):
    return username not in name_id

def is_power_of_two(n):
    """Проверяет, является ли число n степенью двойки."""
    return (n & (n - 1)) == 0 and n != 0


def decoder(data: str) -> tuple[str, int | None]:
    bits = [int(bit) for bit in data]
    tmp = 0
    while 2 ** tmp < len(bits):
        tmp += 1

    posision_error = 0

    # Вычисляем позицию ошибки.
    bits_check = [2 ** i for i in range(tmp)]
    bits_check.reverse()
    for _, bit_check in enumerate(bits_check):
        check = 0
        for j in range(bit_check - 1, len(bits), bit_check * 2):
            check += sum(bits[j:j + bit_check])
        if check % 2 == 1:
            posision_error += bit_check

    # Исправляем ошибку.
    if posision_error > 0:
        bits[posision_error - 1] = 1 - bits[posision_error - 1]

    # Убираем биты проверки.
    decoded_data = ''.join(
        str(bit)
        for i, bit in enumerate(bits)
        if not is_power_of_two(i + 1)
    )

    return (
        decoded_data,
        posision_error - 1 if posision_error > 0 else None,
    )


def split_binary_string(str_binary, part_size=8):
    # Разбиваем строку на части заданного размера
    part = [str_binary[i:i+part_size] for i in range(0, len(str_binary), part_size)]
    # Объединяем части в строку с пробелами
    result = ' '.join(part)
    return result


def binary_to_string(str_binary):
    value_binary = str_binary.split()
    str_ascii = ''.join(chr(int(binary, 2)) for binary in value_binary)
    return str_ascii

def handle_client(socket_client):
    while True:
        data = socket_client.recv(1024).decode('utf-8')
        if not data:
            break

        parts_of_data = data.split(':')
        command = parts_of_data[0]

        if command == 'register':
            username = parts_of_data[1]
            if is_name_unique(username):
                
                len_name = len(name_id)+1                
                
                # user_id = ('0'*(5-len_name))+str(len_name)

                user_id = num_of_zero(len_name)
                name_id[username] = user_id

                clients.append((socket_client, user_id))
                print(f"Registered user '{username}' with id {user_id}")
                socket_client.send(str(user_id).encode('utf-8'))
            else:
                print(f"Error: Username '{username}' is already taken")
                socket_client.send("Username taken".encode('utf-8'))

        elif command == 'send':
            sender_id = int(parts_of_data[1])
            receiver_name = parts_of_data[2]
            encoded_message = parts_of_data[3]
            
            acc3 = decoder(encoded_message)[0]
            acc4 = split_binary_string(acc3)
            message = binary_to_string(acc4)

            if receiver_name in name_id:
                receiver_id = name_id[receiver_name]
                print(f"Message '{message}' sent from '{sender_id}' to '{receiver_name}' (id: {receiver_id})")
                for client in clients:
                    if client[1] == receiver_id:
                        try:
                            client[0].send(f"{receiver_name}:{message}".encode('utf-8'))
                        except OSError as e:
                            print(f"Error sending message to client {receiver_name}: {e}")
                            clients.remove(client)
                socket_client.send("Message delivered".encode('utf-8'))
            else:
                print(f"Error: User '{receiver_name}' not registered")
                socket_client.send("User not registered".encode('utf-8'))

        else:
            print("Invalid command")

    for client in clients:
        if client[0] == socket_client:
            clients.remove(client)
            break

    socket_client.close()


def server_go():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5555))
    server.listen(5)
    print("Server started. Listening on port 5555...")

    while True:
        socket_client, _ = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(socket_client,))
        client_handler.start()


if __name__ == "__main__":
    server_go()