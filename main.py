from pynput import keyboard
import pickle
import csv
import sqlite3

"""
def db():
    c.execute("CREATE TABLE keyboard_counter (key text, counter integer)")
    conn.commit()
    conn.close()
"""

def on_release(key):
    try:
        k = key.char
    except:
        k = key.name

    try:
        print(k)
        track_key(k)
    except Exception as e:
        print(e)

def keyboard_representation(k):
    switcher = {
        "1": "!",
        "2": ['"', "²"]
    }



def track_key(key):
    conn = sqlite3.connect('keyboard_counter.db')
    c = conn.cursor()
    c.execute("SELECT * FROM keyboard_counter WHERE key=?", [key])
    if c.fetchall():
        print("1")
        c.execute("UPDATE keyboard_counter SET counter = counter + 1 WHERE  key=?", [key])
    else:
        print("2")
        c.execute("INSERT INTO keyboard_counter VALUES (?, 1)", [key])

    conn.commit()

    c.execute("SELECT * FROM keyboard_counter")
    print(c.fetchall())
    conn.close()

if __name__ == '__main__':
    #db()

    listener = keyboard.Listener(on_release=on_release)
    listener.start()  # start to listen on a separate thread
    listener.join()  # remove if main thread is polling self.keys
