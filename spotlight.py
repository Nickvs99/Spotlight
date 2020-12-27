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
        pckl_data = create_pckl_data()

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

def create_pckl_data():
    """
    Create a new PickleData object. The object stores the user preferences.
    """

    username = ask_username()

    directory = ask_directory()

    # Since this is the first instance of the pckl_data,
    # set the time to the epoch of time
    pckl_data = PickleData(username, directory, time=0)

    return pckl_data

def ask_username():
    """
    Asks the user for a valid windows username.
    """
    username = input("Your windows username: ")

    while not os.path.isdir(fr"C:\Users\{username}"):
        print(("Invalid windows username. Please enter a valid windows "
               "username. If you are unsure what your username is go towards: "
               r"'C:\Users\'. In this directory will be your windows username."))

        username = input("Your windows username: ")

    return username

def ask_directory():
    """
    Asks the user for a valid designated copy folder.
    """

    print("Select your designated copy folder...")

    directory = filedialog.askdirectory()
    while directory == "":
        print("No selection found. Please select a designated copy folder")
        directory = filedialog.askdirectory()

    return directory


if __name__ == "__main__":
    main()
