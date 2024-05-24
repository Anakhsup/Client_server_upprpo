import socket
import threading

'''
    name_id - словарь, ключ - имя пользователя, значение - уникальный номер;
    clients - список, в котором хранится сокет клиента и его уникальный номер.
'''
name_id = {}
clients = []

def num_of_zero(len_name):
    '''
    Функция генерирует строку, добавляя нужно количество ведущих нулей перед числом len_name.

    Аргументы:
        len_name - длина имени.

    Принцип работы:
        Перед значением len_name ставим нужное количество незначащих нулей в начале строки,
        чтобы получить нужную длину строки в зависимости от значения len_name.
    '''
    return str(len_name).zfill(8)

def is_name_unique(username):
    '''
    Функция проверяет, является ли имя уникальным.

    Аргументы:
        username - имя пользователя;
        name_id - словарь с именами пользователей и их уникальным номеров.
    
    Принцип работы:
        Проверяет уникальность имени пользователя на сервере.
    '''
    return username not in name_id

def is_power_of_two(n):
    """
    Функция проверяет, является ли число n степенью двойки.
    """
    return (n & (n - 1)) == 0 and n != 0

# Как работают инкодер и декодер, для чего нужно проверять число на степень двойки
# Что такое позиция ошибки
def decoder(data: str) -> tuple[str, int | None]:
    '''
    Функция декодирует строку, которая была преобразована алгоритмом Хэмминга.

    Аргументы:
        bits - список битов, где каждый символ строки записан в двоичном виде;
        tmp - проверочный бит;
        bits_check - ;
        check - ;
        posision_error - ;
        decoder_data - ;
    
    Принцип работы:
        Сначала строка data преобразуется в список битов bits, где каждый символ строки преобразуется в его двоичное представление.
        Далее определяется минимальное количество проверочных битов tmp, которые нужно добавить для корректной кодировки данных.
        Определяется позицию ошибки, исправляет её (если она есть) и возвращает исходные данные без проверочных битов.
        Возвращается кортеж из двух элементов: декодированные данные и позицию ошибки (или None, если ошибки нет).
    '''
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
    '''
    Функция разделяет двоичную строку пробелами.

    Аргументы:
        part - часть строки заданного размера;
        result - строка, состоящая из частей, разделенных пробелами.
    
    Принцип работы:
        Разбивается двоичная строка на части заданного размера.
        Возвращается строкаЮ где каждая часть двоичной строки разделена пробелами.
    '''
    # Разбиваем строку на части заданного размера
    part = [str_binary[i:i+part_size] for i in range(0, len(str_binary), part_size)]
    result = ' '.join(part)
    return result


def binary_to_string(str_binary):
    '''
     Функция принимает строку str_binary и конвертирует каждый символ в его ASCII представление.
    
    Аргументы:
        value_binary - переменная для хранения посимвольно закодированной строки;
        str_ascii - переменная, полученная путем конвертации символов из двоичного представления в ASCII.

    Принцип работы:
        Каждый символ строки преобразуется в ASCII представление с помощью (chr(int(binary, 2)).
    '''
    value_binary = str_binary.split()
    str_ascii = ''.join(chr(int(binary, 2)) for binary in value_binary)
    return str_ascii

def handle_client(socket_client):
    '''
    Функция-обработчик клиента, которая выполняется в отдельном потоке для каждого подключения.

    Аргументы:
        parts_of_data - массив, хранящий значения, разбитые через ":";
        command - команда, которую надо выполнить;
        username - имя пользователя;
        sender_id - id отправителя;
        receiver_name - имя отправителя;
        encoded_message - сообщение;
        acc3 - декодированное сообщение;
        acc4 - декодированное сообщение, разделенное пробелами;
        message - сообщение, преобразованное в ASCII;
        receiver_id - id отправителя;
        clients - список кортежей, в котором храняться сокет клиента и его id.

    Принцип работы:
        Принимается сообщения от клиента, разбирается команды (register для регистрации пользователя и send для отправки сообщения).
        Регистрируем новых пользователей, проверяем уникальность имен, отправляем и принимаем сообщения между пользователями.
        Использует функции decoder, split_binary_string, binary_to_string для обработки и отправки данных.

    '''
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
    '''
    Функция, запускающая сервер.

    Аргументы:
        server - сокет;
        client_handler - переменная подключения.

    Принцип работы:
        Создаёт сокет, привязывает его к адресу и начинает слушать входящие подключения.
        Для каждого нового подключения запускает новый поток, который вызывает функцию handle_client.
    '''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    print("Server started. Listening on port 5555...")

    while True:
        socket_client, _ = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(socket_client,))
        client_handler.start()


if __name__ == "__main__":
    server_go()
