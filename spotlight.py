# !/bin/bash python 

import os
import pickle
import time
from shutil import copyfile


windows_spotlight_path = r"temp"
slideshow_path = r"temp"
extension = ".jpg"


def main():

    # Read last time used
    f = open(os.path.join(os.path.dirname(__file__),'store.pckl'), 'rb')
    obj = pickle.load(f)
    f.close()
    last_checked = obj

    count = 0

    for f in os.listdir(windows_spotlight_path):

        if os.path.getmtime(windows_spotlight_path + f) < last_checked:
            continue

        else:
            copyfile(windows_spotlight_path + f, slideshow_path + f + extension)
            count += 1

    print(f"{count} new images added")

    # Write last time used
    f = open(os.path.join(os.path.dirname(__file__),'store.pckl'), 'wb')
    pickle.dump(time.time(), f)
    f.close()

    os.startfile(slideshow_path)

if __name__ == "__main__":
    main()
