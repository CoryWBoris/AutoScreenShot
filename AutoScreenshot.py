#!/usr/bin/env python3
# AutoScreenshot.py

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
import certifi

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
# ublock_path = '/Users/Cory/Documents/ChromeExtScraping/extension_1_49_2_0.crx'
# options.add_extension(ublock_path)
# options.add_argument('--enable-logging')
driver = Chrome(options=options)

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
    file_path = fix_dot_filename(file_path)
    print(f'full path: {file_path}')
    driver.get('https://imgur.com/upload')

    # ideally I will block ads with uBlock origin, but for now I will just close the ad manually
    # ad_close_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.desktop-app.App > div > div.UploadCover > div.Ad-SCTU > div.SctuCloseButton > span > svg > path')))
    # driver.execute_script("arguments[0].click();", ad_close_button)
    
    upload_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#root > div > div.AppDialogs > div > div > div > div > div.PopUpContaner > div.PopUpActions > label")))
    upload_button.click()
    time.sleep(.3)
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

def get_directory():
    # Check if pickle file exists
    if os.path.exists("screenshot.pickle"):
        # Load pickle file
        with open("screenshot.pickle", "rb") as f:
            screenshot_data = pickle.load(f)
        # Check if initialized flag is True
        if screenshot_data.get("Initialized", True):
            screenshot_directory = screenshot_data["screenshot_directory"] 
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
            time.sleep(1)
            os.system('clear')
    # Save screenshot directory to pickle file
    with open("screenshot.pickle", "wb") as f:
        pickle.dump({"Initialized": True, "screenshot_directory": screenshot_directory}, f)
    return screenshot_directory

def extract_timestamp(filename):
    # Regular expression pattern to match the timestamp
    pattern = r'\d{4}-\d{2}-\d{2} at \d{1,2}\.\d{2}\.\d{2} (AM|PM)'
    match = re.search(pattern, filename)
    if match:
        return match.group(0)
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
