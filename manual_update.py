import csv
from config import FILE_NAME
from shared_func import generate_secure_password, readCSV, writeCSV, send_message
#const
PASS_COLLUMN = 3  
#config vars
# Заповнення паролями 
def fill_passwords(data):
    for i in range(1, len(data)):
        data[i][PASS_COLLUMN] = generate_secure_password()
        print(data[i][PASS_COLLUMN])

# Заповнення Шифровання паролів 
def hash_passwords(data): # refactore this
    
    def hash_sha1(password): # refactore this
        import hashlib
        sha1 = hashlib.sha1()
        sha1.update(password.encode('utf-8'))
        return sha1.hexdigest()
    
    for i in range(1, len(data)):  
        if len(data[i]) > PASS_COLLUMN:  
            data[i][PASS_COLLUMN] = hash_sha1(data[i][PASS_COLLUMN])
    writeCSV(FILE_NAME, data)

# Зв'язування номерів з акаунтами // if number doest exist in google
def match_email(data): ## CHECK !!!! REFACTOR
    filename = "SignalTableTest.csv"
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        signalData = []
        for row in csv_reader:
            signalData.append(row)
    signalMailCollumn = 0
    signalNumCollumn = 1
    signalPASS_COLLUMN = 2
    for i in range(1, len(signalData)):
        if not signalData[i][signalNumCollumn]: 
            raise Exception(f"Missing number of user: {signalData[i][0]}")
            #logging.error(f"Missing number of user: {signalData[i][0]}")
        for j in range(1, len(data)):
            if signalData[i][signalMailCollumn] == data[j][2]:
                signalData[i][signalPASS_COLLUMN] = data[j][PASS_COLLUMN]  
                break
        else:
            raise Exception(f"User {signalData[i][signalMailCollumn]} not found") 
            #logging.error(f"Missing number of user: {signalData[i][0]3}")
    writeCSV("SignalTableTest.csv", signalData)
    return signalData

# Розсилка за номерами з SignalTable.csv
def send_all_local_table(signalData):
    signalMailCollumn = 0
    signalNumCollumn = 1
    signalPASS_COLLUMN = 2
    for i in range(1, len(signalData)):
        send_message(signalData[i][signalNumCollumn], signalData[i][signalPASS_COLLUMN], signalData[i][signalMailCollumn])

def send_all_google_table(data):
    MailCollumn = 0
    NumCollumn = 10
    pass_Collumn = 2

    for i in range(1, len(data)):
        if  data[i][NumCollumn]:
            send_message(data[i][NumCollumn], data[i][pass_Collumn], data[i][MailCollumn])
        else:
            print(f"Увага: Неможливо відправити повідомлення для {data[i][MailCollumn]}. Відсутній номер телефону або пароль.")
    

def exe_manual():
    data = readCSV(FILE_NAME)
    fill_passwords(data)
    signalData = match_email(data)
    send_all_local_table(signalData)
    send_all_google_table(data)
    hash_passwords(data)
