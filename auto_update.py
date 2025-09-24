from shared_func import generate_secure_password, send_message
from config import DOMAIN, ORG_UNIT_PATH, SERVICE_ACCOUNT_FILE, SCOPES
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from concurrent.futures import ThreadPoolExecutor
import time
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('admin', 'directory_v1', credentials=creds)
    print("Успішно підключено до Google Admin API.")
except Exception as e:
    print(f"Помилка під час підключення до Google Admin API: {e}")
    exit(1)

def get_all_users():
    """Отримує список усіх користувачів у підрозділі з робочими номерами телефонів."""
    users_data = []
    next_page_token = None
    while True:
        try:
            results = service.users().list(
                domain=DOMAIN,
                maxResults=400,
                pageToken=next_page_token,
                orgUnitPath=ORG_UNIT_PATH,
                projection='full'
            ).execute()

            users = results.get('users', [])
            for user in users:
                email = user.get('primaryEmail')
                phone_number = None

                if 'phones' in user:
                    for phone in user['phones']:
                        if phone.get('type') == 'work' and phone.get('value'):
                            phone_number = phone['value']
                            break  # знайдено робочий номер, виходимо
                        elif not phone_number and phone.get('primary') and phone.get('value'):
                            phone_number = phone['value']

                if email and phone_number:
                    users_data.append({'email': email, 'number': phone_number})
                elif email:
                    logging.warning(f"Пропущено користувача {email} - відсутній робочий або основний номер телефону.")

            next_page_token = results.get('nextPageToken')
            if not next_page_token:
                break

        except Exception as e:
            logging.error(f"Помилка при отриманні користувачів: {e}")
            time.sleep(60)

    return users_data

def create_batches(users, batch_size=200):
    """Розбиває список користувачів на пакети."""
    for i in range(0, len(users), batch_size):
        yield users[i:i + batch_size]

class Batch:
    def __init__(self, batch):
        self.users = batch

    def gen_passwords(self):
        for usr in self.users:
            usr["password"] = generate_secure_password()

    def update_passwords(self):
        for usr in self.users:
            email = usr.get('email')
            password = usr.get('password')
            if email and password:
                try:
                    service.users().patch(userKey=email, body={'password': password}).execute()
                    logging.info(f'Пароль для {email} оновлено успішно.')
                except Exception as e:
                    logging.error(f'Помилка при оновленні пароля для {email}: {e}')
                    time.sleep(60)
                    try:
                        service.users().patch(userKey=email, body={'password': password}).execute()
                    except Exception as e2:
                        logging.error(f'Повторна помилка при оновленні пароля для {email}: {e2}')

            else:
                logging.warning(f"Неможливо оновити пароль для {email or 'невідомо'}: відсутній пароль або email.")

    def send_all(self):
        for usr in self.users:
            email = usr.get('email')
            number = usr.get('number')
            password = usr.get('password')
            if email and number and password:
                try:
                    send_message(number, password, email)
                except Exception as e:
                    logging.error(f"Помилка при відправці повідомлення для {email}: {e}")
            else:
                logging.warning(f"Неможливо відправити повідомлення для {email or 'невідомо'}: відсутній номер або пароль.")

    def process_users(self):
        self.gen_passwords()
        self.update_passwords()
        self.send_all()

def exe_auto():
    print(f"Автоматичний режим запущено для домену: {DOMAIN}, підрозділу: {ORG_UNIT_PATH}")
    all_users = get_all_users()
    print(f"Знайдено {len(all_users)} користувачів для обробки.")

    if not all_users:
        print("Не знайдено користувачів для обробки.")
        return

    batches = list(create_batches(all_users))
    time.sleep(60)
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(lambda batch: Batch(batch).process_users(), batches)

    print("Обробку всіх пакетів завершено.")

if __name__ == '__main__':
    exe_auto()
