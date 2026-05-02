"""
-> একাধিক thead একই সাথে একটি counter increment করার চেষ্টা করবে।
"""

import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    lock.acquire()

    try:
        counter += 1
    finally:
        lock.release()

thread_list = []

for _ in range(100000):
    t = threading.Thread(target=increment)
    thread_list.append(t)
    t.start()

for t in thread_list:
    t.join()

print("Counter with lock (pessimistic locking):", counter)

"""
উপরের code-এর result টি 100000 হওয়ার প্রত্যাশা করা হয় এবং এটি প্রকৃতপক্ষে 100000-ই।
"""
