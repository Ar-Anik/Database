import threading
import time

counter = 0

def increment():
    global counter
    temp = counter

    """
        Because of the GIL Only one thread executes python bytecode at a time.
        For very short operations like counter += 1, one thread often completes the whole sequence before another runs.
        That why we found 100000 right answer by normal code. For race condition we add : time.sleep(0.00001
    """

    time.sleep(0.00001)   # force context switch
    counter = temp + 1

threads = []

for _ in range(100000):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Counter without lock (race condition):", counter)