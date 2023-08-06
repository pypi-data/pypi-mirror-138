# Auther : simplehacker1 simplehacker01 simplehacker02
# Auther : Simplehacker1 Community Group
# Powered by team member :
# Starting Project date : 09/12/2021
# update date  : 12/02/2022
# version : 1.2
# About  : evel encoding decoding Script


import os
import time
import random
import sys

def logo():
    print('''
    EEEEEEEEE  VV        VV  EEEEEEEE   LL        DDDDDDD      CCCCCC
    EE          VV      VV   EE         LL        DD    DD    CC
    EEEEEE       VV    VV    EEEEEE     LL        DD     DD  CC
    EEEEEE        VV  VV     EEEEEE     LL        DD     DD  CC
    EE             VVVV      EE         LLLLLLL   DD    DD    CC
    EEEEEEEEE       VV       EEEEEEEE   LLLLLLLLL DDDDDDD      CCCCCC
    ''')
def eveldc():
    logo()
    eveldc = input("Enter Evel Encoding file :")
    if eveldc == "":
        print("please enter a filename")
    else:
        os.system("mkdir in")
        os.system("cp -r "+eveldc+ " in/")
        with open(eveldc, 'r') as file :
            deta = file.read()
            deta = deta.replace('evel', 'echo')
            with open(eveldc, 'w') as file:
                file.write(deta)
            os.system("bash "+eveldc+ "")
            os.system("cd ..")
            os.system("rm in/* && rm -rf in/")
def loading():
    print("loading .")
    for rajni in range (50):
        sys.stdout.flush()
        time.sleep(3./90)
        print('.', end='')
        time.sleep(2/10)
        print('*', end='')
def Auther():
    print('''
        # Auther : Simplehacker1 Community Group
        # Powered by team member :
        # Starting Project date : 09/12/2021
        # version : 1.1 
        # About  : evel encoding decoding Script'
        #  ''')
def menu():
    loading()
    print("""
    1. sh file encoding
    2. sh evel Decoding
    3. Auther
    4. Exit/Quit
    """)
    menu2=input("Choice A No : ")
    if menu2=="1":
        print("\n Under maintenance")
    elif menu2=="2":
        loading()
        eveldc()
    elif menu2=="3":
        Auther()
    elif menu2=="4":
        print("\n Goodbye")
        exit
    else:
        print("\n Not Valid Choice Try again")


if __name__ == '__main__':
    menu()