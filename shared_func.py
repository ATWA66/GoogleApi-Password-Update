import csv
import subprocess
import secrets
import string
from config import BOT_NUMBER
#прочитати файл
def readCSV(filename): 
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        data = []
        for row in csv_reader:
            data.append(row)
    return data
#Записати в файл
def writeCSV(filename, data):  
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data)
        
def generate_secure_password(length=12):

    if  length < 8:
        length = 8
    elif length > 100:
        length = 100

    letters = string.ascii_letters   
    digits = string.digits        
    all_chars = letters + digits

    password = ''.join(secrets.choice(all_chars) for _ in range(length))
    
    if (any(c in letters for c in password) and
        any(c in digits for c in password)):
        return password
    else:
        return generate_secure_password(length)

def send_message(number, password, mail): # send passwords via signal cli
    try:
        result = subprocess.run(
            ['signal-cli', '-u', '+' + BOT_NUMBER, 'send', number, '-m', f'{password} - ваш новий пароль від корпоративної пошти: {mail}'],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True  # Піднімати виняток для ненульового коду повернення
        )
        print(f"Message sent to {number}: {result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        error_message = f"Помилка відправки повідомлення на {number}: {e.stderr.decode()}"
        print(error_message)

    except FileNotFoundError:
        error_message = "Помилка: Команда 'signal-cli' не знайдена. Переконайтеся, що вона встановлена та доступна в PATH."
        print(error_message)

    except Exception as e:
        error_message = f"Виникла непередбачувана помилка при спробі відправити повідомлення на {number}: {e}"
        print(error_message)
def set_config():
        subprocess.run(
            ['notepad.exe', './config.py'],
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True  # Піднімати виняток для ненульового коду повернення
        )
    
        """
def deletemsg():
    import subprocess
    try:
        # Команда для получения списка отправленных сообщений
        receive_command = f'signal-cli -u "{BOT_NUMBER}" receive'
        received_output = subprocess.check_output(receive_command, shell=True).decode('utf-8', errors='ignore')
        print("1stage")
        # Парсинг сообщений и удаление каждого
        for line in received_output.splitlines():
            if '"timestamp":' in line:
                # Извлечение идентификатора сообщения
                timestamp = line.split(":")[1].strip().replace(",", "")
                # Удаление сообщения
                delete_command = f'signal-cli -u "{BOT_NUMBER}" remoteDelete -t {timestamp}'
                subprocess.run(delete_command, shell=True)
                print(f"Удалено сообщение с меткой времени: {timestamp}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
"""

