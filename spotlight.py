# !/bin/bash python 

import os
import pickle
import time
from tkinter import Tk
from tkinter  import filedialog
from shutil import copyfile

extension = ".jpg"
file_path = os.path.dirname(__file__)

def main():

    # Check if a store.pckl file exists
    if os.path.isfile(os.path.join(file_path,'store.pckl')):

        f = open(os.path.join(file_path,'store.pckl'), 'rb')
        pckl_data = pickle.load(f)
        f.close()
    else:

        username = input("Your windows username: ")

        print("Select your designated copy folder...")
        Tk()
        directory = filedialog.askdirectory()

        # Since this is the first instance of the pckl_data,
        # set the time to the epoch of time
        pckl_data = PickleData(username, directory, time=0)

    windows_spotlight_path = fr"C:\Users\{pckl_data.username}\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets\\"
    
    count = 0
    for f in os.listdir(windows_spotlight_path):

        if os.path.getmtime(windows_spotlight_path + f) < pckl_data.time:
            continue

        else:
            copyfile(windows_spotlight_path + f, os.path.join(pckl_data.directory, f + extension))
            count += 1

    print(f"{count} new images added")

    pckl_data.update_time()
    pckl_data.dump()

    os.startfile(pckl_data.directory)

class PickleData():

    def __init__(self, username, directory, time=time.time(), filename="store.pckl"):
        
        self.username = username
        self.directory = directory
        self.time = time

        self.dump(filename=filename)

    def update_time(self):
        self.time = time.time()


    def dump(self, filename="store.pckl"):
        f = open(os.path.join(file_path, filename), 'wb')
        pickle.dump(self, f)
        f.close()

if __name__ == "__main__":
    main()
