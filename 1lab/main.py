import socket

# Создание TCP/IP сокета
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключение к серверу
server_address = ('localhost', 8000)
client_socket.connect(server_address)
def save_xml_to_file(xml_string, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as xml_file:
            xml_file.write(xml_string)  # Запись строки в файл
        print(f"XML сохранен в файл: {file_path}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
def get_data(client_socket):
    data = bytearray()
    while True:
        chunk = client_socket.recv(1024)
        data.extend(chunk)
        if b'\0' in chunk:
            break
    return data
print("Приветствую, готов работать")
message=""
while True:   
    message=input("Введите команду:").strip()
    try:
        client_socket.sendall(message.encode())
        if(message=="close"):
            client_socket.close()
            break
        data=get_data(client_socket)
        header=data[:3].decode('utf-8')
        xml_bytes = data[3:-1]
        result_string = xml_bytes.decode('utf-8')
        if(header=="xml"):
            save_xml_to_file(result_string, "./process.xml")
            print("Результат в файле process.xml")
        else:
            print(result_string)
    except:
        pass