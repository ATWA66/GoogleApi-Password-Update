import sys
from manual_update import exe_manual
#from auto_update import exe_auto
from shared_func import set_config
import logging 
logging.basicConfig(filename='errors.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')
#config
def main():
    if len(sys.argv) == 1:
        pass
        #exe_auto()

    elif sys.argv[1] == '-c' or sys.argv == '--config'and len(sys.argv) == 2:
        set_config()
        
    elif sys.argv[1] == '-h' or sys.argv == '--help'and len(sys.argv) == 2:
        print("flag list:\n-m to run csv mode\n-c to open configuration\n-h to see help \nend of flaglist\n")
        
    elif sys.argv[1] == '-m' or sys.argv == '--manual' and len(sys.argv) == 2:
        pass
        #exe_manual()

    else:
        print("wrong parameters, check -h or --help to see parameters list.")
'''
    fileName = 'users.csv'
    data = readCSV(fileName)
    control = '0'
    print("--menu--\n1. Generate files(w/decripted passwords & encrypted)\n2. Send all passwords\n3.delete messages\n4. Exit")
    while control != '4':
        control = input()
        if control == 1:
            fill_passwords(data)
            signalData = match_email(data)
            hash_passwords(data)
            print(data[1][PASSCOLLUMN])  # Перевірка паролю після генерації
        elif control == '2':
            send_all(signalData)
        elif control == '3':
            deletemsg()
        elif control == '4':
            print("job done, have a good day")
        else:
            print("wrong input, try again!")
'''
if __name__ == "__main__":
    main()