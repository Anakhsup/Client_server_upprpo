import socket

# Что такое сокет?
def encoder(data: str) -> str:
    '''
    Функция принимает строку data и кодирует её в более длинную строку с использованием кода Хэмминга.
    
    Аргументы:
        bits - список битов, где каждый символ строки записан в двоичном виде;
        tmp - проверочный бит;
        result - массив с битами и проверочными битами кода Хэмминга.
    
    Принцип работы:
        Сначала строка data преобразуется в список битов bits, где каждый символ строки преобразуется в его двоичное представление.
        Далее определяется минимальное количество проверочных битов tmp, которые нужно добавить для корректной кодировки данных.
        Создаётся массив result, в который помещаются биты и проверочные биты кода Хэмминга.
        Функция возвращает закодированную строку в виде строки битов.
    '''

    bits = [int(bit) for bit in data]
    tmp = 0
    while 2 ** tmp < len(bits) + tmp + 1:
        tmp += 1

    result = [0] * (len(bits) + tmp)
    j = 0
    for i in range(len(result)):
        if i + 1 == 2 ** j:
            j += 1
        else:
            result[i] = bits.pop(0)

    for i in range(tmp):
        posision = 2 ** i - 1
        check = 0
        for j in range(posision, len(result), 2 * posision + 2):
            check ^= result[j:j + posision + 1].count(1) % 2
        result[posision] = check

    return ''.join([str(bit) for bit in result])


def string_to_binary(string):
    '''
    Функция принимает строку string и конвертирует каждый символ в его двоичное представление, в виде строки из нулей и единиц.
    
    Аргументы:
        binary_result - массив для хранения посимвольно закодированной строки.

    Принцип работы:
        Каждый символ строки преобразуется в двоичное представление с помощью format(ord(char), '08b'), где ord(char) возвращает числовое значение символа.
    '''

    binary_str = ' '.join(format(ord(char), '08b') for char in string)
    return binary_str

def connect_binary_strings(binary_str):
    '''
    Функция принимает строку binary_str, которая содержит двоичные представления символов, разделённые пробелами.

    Аргументы:
        binary_list - разделенное двоичное представление строки;
        connect_string - объединенное двоичное представление входной строки.

    Принцип работы:
        Сначала строка binary_str разделяется на отдельные двоичные представления с помощью .split().
        Затем эти отдельные двоичные представления объединяются в одну строку без пробелов с помощью .join() и возвращаются как результат.
    '''

    binary_list = binary_str.split()
    connect_string = ''.join(binary_list)
    return connect_string


def register_user(username):
    '''
    Функция регистрирует пользователя на сервере.

    Аргументы:
        socket_client - сокет;
        response - id пользователя.

    Принцип работы:
        Создаётся сокет socket_client, который подключается к серверу.
        Отправляется запрос на сервер.
        Получается ответ от сервера и проверяется, занят ли выбранный username.

    '''

    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect(('127.0.0.1', 5555))
    socket_client.send(f"register:{username}".encode('utf-8'))
    response = socket_client.recv(1024).decode('utf-8')
    if response == "Username taken":
        print("Error: Username is already taken. Please choose a different one.")
        socket_client.close()
        return None
    else:
        print(f"Registered successfully. Your id is: {response}")
        socket_client.close()
        return response

def send_message(sender_id, receiver_name, message):
    '''
    Функция отправляет сообщение от отправителя к получателю.

    Аргументы:
        acc - конвертироанная строка;
        acc2 - объединенная конвертированная строка;
        encoded_message - закордированная строка с помощью алгоритма Хэмминга.

    Принцип работы:
        Сообщение сначала конвертируется в двоичную строку с помощью функции string_to_binary, затем объединяется без пробелов с помощью connect_binary_strings.
        Полученная строка битов кодируется с использованием функции encoder.
        Создаётся сокет.
        Отправляется запрос на сервер в формате.
        Получается ответ от сервера и выводится на экран.
    '''

    acc = string_to_binary(message)
    acc2 = connect_binary_strings(acc)
    encoded_message = encoder(acc2)

    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect(('127.0.0.1', 5555))
    socket_client.send(f"send:{sender_id}:{receiver_name}:{encoded_message}".encode('utf-8'))
    response = socket_client.recv(1024).decode('utf-8')
    print("Server response:", response)
    socket_client.close()

if __name__ == "__main__":
    username = input("Enter your username: ")
    user_id = None
    while user_id is None:
        user_id = register_user(username)
        if user_id is None:
            username = input("Enter a different username: ")
    while True:
        receiver_name = input("Enter receiver's username or 'exit': ")
        if receiver_name == 'exit':
            break
        message = input("Enter message: ")
        send_message(user_id, receiver_name, message)
