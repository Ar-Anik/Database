import threading

counter = 0
lock = threading.Lock()

def increment():
    global counter
    with lock:
        counter += 1

thread_list = []

for _ in range(100000):
    t = threading.Thread(target=increment)
    thread_list.append(t)
    t.start()

for t in thread_list:
    t.join()

print("Counter with lock (pessimistic locking):", counter)
