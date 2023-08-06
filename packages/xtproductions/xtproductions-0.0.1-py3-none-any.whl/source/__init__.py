import time

def bl(n):
    return [_ for _ in range(10 ** n)]

def tstart():
    return time.time()

def tend():
    return time.time() - tstart()
