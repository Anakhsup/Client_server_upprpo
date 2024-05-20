import socket


def encoder(data: str) -> str:
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
    binary_str = ' '.join(format(ord(char), '08b') for char in string)
    return binary_str

def connect_binary_strings(binary_str):
    binary_list = binary_str.split()
    connect_string = ''.join(binary_list)
    return connect_string


def register_user(username):
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
        receiver_name = input("Enter receiver's username (or 'exit' to quit): ")
        if receiver_name == 'exit' or receiver_name == 'exit ':
            break
        message = input("Enter message: ")
        send_message(user_id, receiver_name, message)