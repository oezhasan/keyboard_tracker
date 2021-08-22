from pynput import keyboard
import pickle
import atexit

dict = pickle.load(open("save.p", "rb"))


def on_release(key):
    print(dict)
    try:

        k = key.char
    except:
        k = key.name

    try:
        track_key(k)

    except:
        pass

def track_key(k):
    if k in dict:
        dict[k] += 1
    else:
        dict[k] = 1

def exit_handler():
    print(dict)
    pickle.dump(dict, open("save.p", "wb"))


atexit.register(exit_handler)
listener = keyboard.Listener(on_release=on_release)
listener.start()  # start to listen on a separate thread
listener.join()  # remove if main thread is polling self.keys
