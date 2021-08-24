from pynput import keyboard
import pickle
import atexit
import csv

d = {}

def open_csv():
    reader = csv.reader(open('keyboard_tracker.csv', 'r'))
    for k,v in reader:
        d[k] = v

def on_release(key):
    try:
        k = key.char
    except:
        k = key.name

    try:
        track_key(k)
        print(k)
    except:
        pass

def track_key(k):
    if k in d:
        d[k] += 1
    else:
        d[k] = 1

def save_csv():
    with open('keyboard_tracker.csv', 'wb') as output:
        writer = csv.writer(output)
        for k, v in d.items():
            writer.writerow([k, v])

if __name__ == '__main__':
    try:
        open_csv()
        listener = keyboard.Listener(on_release=on_release)
        listener.start()  # start to listen on a separate thread
        listener.join()  # remove if main thread is polling self.keys
    finally:
        print("Programm beendet")
        save_csv()