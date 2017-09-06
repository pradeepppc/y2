import threading
class messanger(threading.Thread):
    def run(self):
        for _ in range(10000):
            print(threading.current_thread().getName())

x = messanger(name='send messsage')
y = messanger(name='recieve message')
x.start()
y.start()