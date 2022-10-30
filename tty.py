import threading
from time import sleep

r = 0
lock = threading.Lock()
def p1():
    global r
    r += 1
    s()
    # sleep(10)


def s():
    global r
    if r == 1:
        # r -= 1
        lock.acquire()
        print("1 running")
        sleep(15)
        print("1 releasing")
        r -= 1
        lock.release()

    if r == 1:
        # r -= 1
        lock.acquire()
        print("2 running")
        sleep(15)
        print("2 releasing")
        r -= 1
        lock.release()

while True:
    sleep(15)
    print("Called")
    p = threading.Thread(target=p1)
    p.start()