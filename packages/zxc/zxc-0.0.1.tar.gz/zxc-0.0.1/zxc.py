import time
import threading

i = 1000

def setNum(num):
    global i
    i = num

def _zxc_math(delay=0.2):
    global i
    print("Zxc math passer by.Fikko ;)")
    while i >= 7:
        i = i - 7
        print(i)
        time.sleep(delay)

def zxc_math(delay=0.2,action=False,thread=False):
    global i
    if action == True:
        init = input("Start ? [Y/n] : ")
        if init == "Y" or init == "y" or init == "Н" or init == "н":
            if thread == True:
                x = threading.Thread(target=_zxc_math)
                x.start()
            elif thread == False:
                print("Zxc math passer by.Fikko ;)")
                while i >= 7:
                    i = i - 7
                    print(i)
                    time.sleep(delay)
        else:
            print("programm exit!!")
    elif action == False:
        if thread == True:
            x = threading.Thread(target=_zxc_math)
            x.start()
        elif thread == False:
            print("Zxc math passer by.Fikko ;)")
            while i >= 7:
                i = i - 7
                print(i)
                time.sleep(delay)
