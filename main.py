import time

from Engine import Engine

if __name__ == '__main__':
    engine = Engine()
    start = time.time()
    engine.start()
    print(time.time() - start)