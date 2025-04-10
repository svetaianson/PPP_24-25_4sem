import asyncio
import os
import pandas as pd
import logging
import sys
class sesion:
    def __init__(self, name):
        self.name = name
        self.context = str(name)
    def windows(self,data):
        os.system('chcp 65001 > nul 2>&1')
        if(data.replace(" ","") == "list"):
            stream = os.popen('tasklist')
            output = stream.read().replace("В\xa0", "").split("\n")[3:]
            to_exel = [i.split() for i in output]
            process = [i[0] for i in to_exel[:-1]]
            pid = [i[1] for i in to_exel[:-1]]
            typ = [i[2] for i in to_exel[:-1]]
            user = [i[3] for i in to_exel[:-1]]
            potok = [i[4] for i in to_exel[:-1]]
            kol = [i[5] for i in to_exel[:-1]]
            data = {
                'Процесс': process,
                'PID': pid,
                'Тип': typ,
                'Пользователь':user,
                'Поток':potok,
                'К':kol
            }
            df = pd.DataFrame(data)
            xml_data = df.to_xml(root_name = 'processes', row_name = 'process', index = False, encoding = 'utf-8')
            xml_bytes = xml_data.encode('utf-8')
            header = "xml".encode('utf-8')
            packet = header+ xml_bytes + b'\0'
            self.context += ">list"
            return packet
        elif(data.replace(" ","") == "help"):
            header = "com".encode('utf-8')
            self.context += ">help"
            return header + '''
Команды:
list - выводит процессы и сохраняет их в формате xml.
SIGTERM pid - Завершения проценна корректно. Вместо id нужно указать pid процесса.
SIGKILL pid - Принудительное завершение процесса. Вместо id нужно указать pid процесса.
                '''.encode('utf-8') + b'\0'
        elif "SIGTERM" in data or "sigterm" in data:
            data = data.repalce(" ",'')
            id = data.replace("SIGTERM","")
            id = data.replace("sigterm","")
            header = "com".encode('utf-8')
            self.context += f'>SIGTERM {id}'
            try:
                os.system(f'taskkill /PID {id} /T /F')
                return header + "Успешно".encode('utf-8') + b'\0'
            except:
                return header + "Ошибка синтаксиса, не верно указан pid".encode('utf-8') + b'\0'
        elif "SIGKILL" in data or "sigkill" in data:
            id = data.replace("SIGKILL","")
            id = data.replace("sigkill","")
            header = "com".encode('utf-8')
            self.context += f'>SIGKILL {pid}'
            try:
                os.system(f'taskkill /F /Ppid {pid}')
                return header + "Успешно".encode('utf-8') + b'\0'
            except:
                return header + "Ошибка синтаксиса, не верно указан ppid".encode('utf-8') + b'\0'
        else:
            header="com".encode('utf-8')
            self.context += '>Error'
            return header + "Ошибка синтаксиса, введите команду help для подсказки".encode('utf-8') + b'\0'
    def linux(self,data):
        os.system('export LANG=en_US.UTF-8')
        os.system('export LC_ALL=en_US.UTF-8')
        if data.replace(" ","") == "help":
            self.context += ">help"
            header = "com".encode('utf-8')
            return header + '''
Команды:
list - выводит процессы и сохраняет их в формате xml.
SIGINT pid - Прерывает процесс и выполняет очистку перед завершением. Вместо pid нужно указать pid процесса.
SIGHUP pid - Перезагружает процесс. Вместо pid нужно указать pid процесса.
SIGQUIT pid - Используется для завершения процесса и создания дампа памяти. Вместо pid нужно указать pid процесса.
SIGSTOP pid - Останавливает (приостанавливает) процесс. Вместо pid нужно указать pid процесса.
SIGCONT pid - Возобновляет выполнение приостановленного процесса. Вместо pid нужно указать pid процесса.
SIGTERM pid - Завершения проценна корректно. Вместо pid нужно указать pid процесса.
SIGKILL pid - Принудительное завершение процесса. Вместо pid нужно указать pid процесса.
                '''.encode('utf-8') + b'\0'
        elif(data.replace(" ","") == "list"):
            stream = os.popen('ps aux')
            output = stream.read()
            self.context += ">list"
            to_exel = [i.split() for i in output[1:-1]]
            process = [i[0] for i in to_exel[:-1]]
            ppid = [i[1] for i in to_exel[:-1]]
            typ = [i[2] for i in to_exel[:-1]]
            user = [i[3] for i in to_exel[:-1]]
            potok = [i[4] for i in to_exel[:-1]]
            kol = [i[5] for i in to_exel[:-1]]
            kol2 = [i[6] for i in to_exel[:-1]]
            kol3 = [i[7] for i in to_exel[:-1]]
            data = {
                'Ppid': process,
                'PPpid': ppid,
                'PGpid': typ,
                'WINPpid':user,
                'TTY':potok,
                'Upid':kol,
                'STIME':kol2,
                'COMMAND':kol3
            }
            df = pd.DataFrame(data)
            xml_data = df.to_xml(root_name = 'processes', row_name = 'process', index = False, encoding = 'utf-8')
            xml_bytes = xml_data.encode('utf-8')
            header = "xml".encode('utf-8')
            packet = header+ xml_bytes + b'\0'
            self.context += ">list"
            return packet
            
        elif "SIGINT" in data or "sigint" in data:
            data = data.repalce(" ",'')
            pid = data.replace("SIGINT","")
            pid = data.replace("sigint","")
            self.context += f'>SIGINT {pid}'
            header = "com".encode('utf-8')
            try:
                os.system(f'kill -SIGINT {pid}')
                return "Успешно".encode('utf-8') + b'\0'
            except:
                return header + "Ошибка синтаксиса, не верно указан pid".encode('utf-8')+ b'\0'

        elif "SIGHUP" in data or "sighup" in data:
            data = data.repalce(" ",'')
            pid = data.replace("SIGHUP","")
            pid = data.replace("sighup","")
            self.context += f'>SIGHUP {pid}'
            header = "com".encode('utf-8')
            try:
                os.system(f'kill -SIGHUP {pid}')
                return header + "Успешно".encode('utf-8') + b'\0'
            except:
                return header + "Ошибка синтаксиса, не верно указан pid".encode('utf-8') + b'\0'

        elif "SIGQUIT" in data or "sigquit" in data:
            data = data.repalce(" ",'')
            pid = data.replace("SIGQUIT","")
            pid = data.replace("sigquit","")
            self.context+=f'>SIGQUIT {pid}'
            header = "com".encode('utf-8')
            try:
                os.system(f'kill -SIGQUIT {pid}')
                return header + "Успешно".encode('utf-8') + b'\0'
            except:
                return header + "Ошибка синтаксиса, не верно указан pid".encode('utf-8') + b'\0'
        elif "SIGSTOP" in data or "sigstop" in data:
            data = data.repalce(" ",'')
            pid = data.replace("SIGSTOP","")
            pid = data.replace("sigstop","")
            self.context+=f'>SIGSTOP {pid}'
            header = "com".encode('utf-8')
            try:
                os.system(f'kill -SIGSTOP {pid}')
                return header + "Успешно".encode('utf-8') + b'\0'
            except:
                return header + "Ошибка синтаксиса, не верно указан pid".encode('utf-8') + b'\0'
        elif "SIGCONT" in data or "sigcont" in data:
            data = data.repalce(" ",'')
            pid = data.replace("SIGCONT","")
            pid = data.replace("sigcont","")
            self.context += f'>SIGCONT {pid}'
            header = "com".encode('utf-8')
            try:
                os.system(f'kill -SIGCONT {pid}')
                return header + "Успешно".encode('utf-8') + b'\0'
            except:
                return header+"Ошибка синтаксиса, не верно указан pid".encode('utf-8') + b'\0'
        elif "SIGTERM" in data or "sigterm" in data:
            data = data.repalce(" ",'')
            pid = data.replace("SIGTERM","")
            pid = data.replace("sigterm","")
            self.context += f'>SIGTERM {pid}'
            header = "com".encode('utf-8')
            try:
                os.system(f'kill -SIGTERM {pid}')
                return header + "Успешно".encode('utf-8') + b'\0'
            except:
                return header + "Ошибка синтаксиса, не верно указан pid".encode('utf-8') + b'\0'
        elif "SIGKILL" in data or "sigkill" in data:
            data = data.repalce(" ",'')
            pid = data.replace("SIGKILL","")
            pid = data.replace("sigkill","")
            self.context += f'>SIGKILL {pid}'
            header = "com".encode('utf-8')
            try:
                os.system(f'kill -SIGKILL {pid}')
                return header+"Успешно".encode('utf-8') + b'\0'
            except:
                return header+"Ошибка синтаксиса, не верно указан pid".encode('utf-8') + b'\0'
        else:
            self.context += ">Error"
            header = "com".encode('utf-8')
            return header + "Ошибка синтаксиса, введите команду help для подсказки".encode('utf-8') + b'\0'
async def client(reader, writer):
    addr = writer.get_extra_info('peername')
    user=sesion(addr)
    while (data := (await reader.read(100)).decode()) != "close":
        if data != "":
            print(data)
            if os.name == 'posix':
                answer = await user.linux(data.replace(" ",""))
                writer.write(answer.encode())
                await writer.drain()
            else:
                answer = user.windows(data.replace(" ",""))
                writer.write(answer)
                await writer.drain()
    logging.info(user.context + ">close" + "\n")
    writer.close()
    await writer.wait_closed()
    return 0

async def main():
    logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s', handlers = [
    logging.StreamHandler(sys.stdout),
    logging.FileHandler("./server.log")])
    logging.info("Сервер запущен и ждет подключения...")
    server = await asyncio.start_server(client, 'localhost', 8000)
    async with server:
        await server.serve_forever()

asyncio.run(main())