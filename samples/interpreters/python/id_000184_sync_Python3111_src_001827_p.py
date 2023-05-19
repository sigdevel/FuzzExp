

try:
    import utime

    sleep_ms = utime.sleep_ms
except ImportError:
    import time

    sleep_ms = lambda t: time.sleep(t / 1000)
import _thread


def thread_entry(n):
    pass


thread_num = 0
while thread_num < 500:
    try:
        _thread.start_new_thread(thread_entry, (thread_num,))
        thread_num += 1
    except (MemoryError, OSError) as er:
        
        
        sleep_ms(50)


sleep_ms(500)
print("done")
