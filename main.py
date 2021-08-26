from pynput import keyboard
import pickle
import csv
import sqlite3

def db():
    c.execute("CREATE TABLE keyboard_counter (key text, counter integer)")
    conn.commit()
    conn.close()




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



def track_key(variable):
    conn = sqlite3.connect('keyboard_counter.db')
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM keyboard_counter WHERE key = {}".format(variable))
        conn.commit()
        c.execute("UPDATE keyboard_counter SET counter = counter + 1 WHERE  key={}".format(variable))
        conn.commit()

    except Exception as e:
        print(e)
        c.execute("INSERT INTO keyboard_counter VALUES ({}, 1)".format(variable))
        conn.commit()


    conn.close()





if __name__ == '__main__':
    #db()
    """
    c.execute("SELECT * FROM keyboard_counter")
    print(c.fetchall())
    conn.commit()
    conn.close()
    """

    listener = keyboard.Listener(on_release=on_release)
    listener.start()  # start to listen on a separate thread
    listener.join()  # remove if main thread is polling self.keys
