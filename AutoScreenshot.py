#!/usr/bin/env python3
# AutoScreenshot.py

import certifi
import datetime
import os
import pickle
import random
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchWindowException, TimeoutException
from selenium.webdriver import ActionChains
import ssl
import subprocess
import time
from undetected_chromedriver import Chrome, ChromeOptions
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


# ___________________________________________________________________________________________________________________________________________________________
# I had to fire my very high graphics designer
os.system('clear')
print("        +========================+")
print("        |                        |")
print("        |    AUTO SCREEN SHOT    |")
print("        |           By           |")
print("        |       Cory Boris       |")
print("        |       MIT License      |")
print("        |          ©2023         |")
print("        |________________________|")
print("        |            ( + ) ( - ) |")
print("        +========================+")
print("              /       |    \\")
print("             /        |     \\")
print("            /         |      \\")
print("           /                  \\")
print("          /                    \\\n")
time.sleep(3.5)
os.system('clear')
# ___________________________________________________________________________________________________________________________________________________________

# This global block is the code which allows the user to input the directory for their adBlock plugin. 
# You can use any ad blocker though, but uBlock is really really good.

# Check if pickle file contains string already for adblocker:
if os.path.exists("directories.pickle"):
    # Load pickle file
    with open("directories.pickle", "rb") as f:
        pickle_data = pickle.load(f)
    # Check if initialized flag is True
    if pickle_data.get("Initialized adBlock Directory", False):
        adBlock_directory = pickle_data["adBlock_directory"]
        if os.path.isdir(adBlock_directory):
            pass
        else:
            print("Not valid adBlock directory. Delete pickle file and restart program.") 
            exit(1)
    else:
        print("adBlock Directory not properly initialized. Delete pickle file and restart program.") 
        exit(1)


else:
    # If pickle file doesn't exist, prompt user for directory
    while True:
        os.system('clear')  
        adBlock_directory = input("Please enter adBlock add-on directory: ")
        if os.path.isdir(adBlock_directory):
            break
        else:
            os.system('clear')
            print("Sorry, that directory is not valid, please try again.")
            time.sleep(2)
            os.system('clear')
    # Save screenshot directory to pickle file
    with open("directories.pickle", "wb") as f:
        pickle.dump({"Initialized adBlock Directory": True, "adBlock_directory": adBlock_directory}, f)

# ____________________________________________________________________________________________________________________________________

# verify ssl certificate
os.environ['SSL_CERT_FILE'] = certifi.where()

# Set up Chrome options
options = ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--no-sandbox')

# Disable password saving prompt for the loaded profile
prefs = {
    'credentials_enable_service': False,
    'profile.password_manager_enabled': False
}
options.add_experimental_option('prefs', prefs)
options.add_argument(f'--load-extension={adBlock_directory}')
driver = Chrome(options=options)

# _____________________________________________________________________________________________________________________________________

class MyHandler(FileSystemEventHandler):
    def __init__(self, main_dir):
        self.main_dir = main_dir
        self.last_check_time = datetime.datetime.now()

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.jpg') and os.path.isfile(event.src_path):
            file_path = event.src_path
            file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_time > self.last_check_time:
                print(file_path)
                self.last_check_time = file_time  # update last check time
                file_path = fix_dot_filename(file_path)
                args = (file_path,)
                go_to_imgur_upload(file_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.jpg') and os.path.isfile(event.src_path):
            file_path = event.src_path
            file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_time > self.last_check_time:
                self.last_check_time = file_time  # update last check time
                file_path = fix_dot_filename(file_path)
                args = (file_path,)
                go_to_imgur_upload(file_path)

def fix_dot_filename(filepath):
    directory, filename = os.path.split(filepath)
    if filename.startswith('.'):
        fixed_filename = filename[1:]
        fixed_filepath = os.path.join(directory, fixed_filename)
        return fixed_filepath
    return filepath

def go_to_imgur_upload(file_string):
    print("uploading image:")

    # On apple, screenshots are autoamtically named with the timestamp included. 
    # But when using watchdog, the filename has a slightly different timestamp in its name, even though it is referring to the same file
    # The following is how I get the most recent screenshot in spite of the name of watchdog's filename not having the same time stamp as the file's name itself
    # if the file's name is not exact then i can't press enter for the file dialogue window and the program will crash
    # but this code guarantees that you upload the most recent screenshot, which is the whole point.
    directory = os.path.dirname(file_string)
    files = os.listdir(directory)

    # this blasted dot in the filename is causing me so much trouble
    for i, file in enumerate(files):
        if file[0] == '.':
            files[i] = file[1:]
    files = [file for file in files if not file.endswith('DS_Store')]
    files = [file for file in files if extract_timestamp(file) is not None]
    # print(files)
    # Sort files in directory by creation time
    files.sort(key=extract_timestamp)

    # Get the filename of the most recently created file
    most_recent_file = files[-1]


    file_path = directory + "/" + most_recent_file
    # this is possibly redundant but believe it or not, I'm traumatized by the inundation of dots I have been experiencing while making this script
    file_path = fix_dot_filename(file_path)
    print(f'full path of screenshot: {file_path}')
    driver.get('https://imgur.com/upload')
    
    upload_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > div.AppDialogs > div > div > div > div > div.PopUpContaner > div.PopUpActions > label")))
    upload_button.click()
    time.sleep(.3)

    # I couldn't do this with javascript, and I didn't absolutely need to, but it would be cool to do that in order to make the script more compatible
    process = subprocess.run([
        "osascript",
        "-e", 'tell application "Google Chrome" to activate',
        "-e", 'tell application "System Events"',
        "-e", 'keystroke "g" using {shift down, command down}',
        "-e", 'delay 1.5',
        "-e", f'keystroke "{file_path}" & return',
        "-e", 'delay 1.5',
        "-e", 'keystroke return',
        "-e", 'end tell'
    ])
    
    toast_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "Toast-message--check")))
    actions = ActionChains(driver)
    img_container = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > div.desktop-app.App > div > div.Upload-container > div.UploadPost > div > div:nth-child(2) > div.PostContent-imageWrapper > div.PostContent-imageWrapper-rounded > img")))
    actions.move_to_element(img_container).perform()
    copy_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > div.desktop-app.App > div > div.Upload-container > div.UploadPost > div > div.PostContent.UploadPost-file > div.PostContent-imageWrapper > div.PostContentMenu > button")))
    copy_button.click()


# Long note if you are curious why I have a single global instance of getting a user input and the same method defined globally:
# While it may seem redundant, and it probably is in terms of efficiency, I couldn't think of a way to overcome the limitation
# introduced by using a driver globally in the first place, and there is no way around this since my code is triggered by an event 
# listener which runs into threading issues when I initialize the driver from the event listener itself rather than globally as I have done in my code
# Ideally, I could have recycled the code from get_directory but I couldn't in this case since I needed to call the driver globally, and I need the directory of the ad blocker 
# in order to use chrome which all happens before the event listener and obtaining the file directory for that.
def get_directory():
    # Check if pickle file exists
    if os.path.exists("directories.pickle"):
        # Load pickle file
        with open("directories.pickle", "rb") as f:
            pickle_data = pickle.load(f)
            # Check if initialized flag is True
            if pickle_data.get("Initialized Screenshot Directory", False):
                screenshot_directory = pickle_data["screenshot_directory"] 
                if os.path.isdir(screenshot_directory):
                    return screenshot_directory  
                else:
                    print("Corrupted screenshot directory. Delete pickle file and restart program.") 
                    exit(1)

    # If pickle file doesn't exist, prompt user for directory
    while True:
        os.system('clear')  
        screenshot_directory = input("Please enter screenshot directory: ")
        if os.path.isdir(screenshot_directory):
            break
        else:
            os.system('clear')
            print("Sorry, that directory is not valid, please try again.")
            time.sleep(2)
            os.system('clear')
    # Save screenshot directory to pickle file
    pickle_data = {"Initialized Screenshot Directory": True, "screenshot_directory": screenshot_directory}
    if os.path.exists("directories.pickle"):
        with open("directories.pickle", "rb") as f:
            old_pickle_data = pickle.load(f)
        pickle_data.update(old_pickle_data)
    with open("directories.pickle", "wb") as f:
        pickle.dump(pickle_data, f)
    return screenshot_directory

def extract_timestamp(filename):
    # Regular expression pattern to match the timestamp
    pattern = r'\d{4}-\d{2}-\d{2} at \d{1,2}\.\d{2}\.\d{2} (AM|PM)'
    match = re.search(pattern, filename)
    if match:
        # Extract the date and time from the match
        timestamp_str = match.group(0)
        date_str, time_str = timestamp_str.split(' at ')

        # Convert the date and time strings into a datetime object
        timestamp = time.strptime(timestamp_str, '%Y-%m-%d at %I.%M.%S %p')

        return timestamp
    return None


def main():
    # Get the main directory to watch as a command line argument
    main_dir = get_directory()
    # Create a file system event handler
    event_handler = MyHandler(main_dir)
    print("started event handler")

    # Create a watchdog observer to watch the main directory
    observer = Observer()
    observer.schedule(event_handler, main_dir, recursive=True)

    # Start the observer
    observer.start()


    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

if __name__ == '__main__':

    main()
