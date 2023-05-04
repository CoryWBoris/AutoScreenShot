# AutoScreenShot.py by Cory Boris
A simple Python script for Mac OSX for uploading images to Imgur using undetected-chromedriver which uses Selenium via Chrome.

## Requirements
Python 3 (https://www.python.org/downloads/) 
selenium  
undetected-chromedriver  
watchdog  
certifi
Latest Version of Google Chrome

## Installation
Clone or download this repository.
Then install the required packages: 
pip install selenium watchdog undetected-chromedriver certifi

## Usage
For first time use, run the script in terminal: python3 AutoScreenshot.py  
A selenium instance of chrome will open, and then you will be prompted to enter the directory of your screenshot. 
After your enter your directory, you will see "started event handler" and you are good to go and ready for general use.  

General Use:
If your directory is already entered the first time, then you will just see selenium's instance of Google Chrome open and the same "started event handler" message. 
When a new image is added to the specified directory, the script will automatically upload it to Imgur.com/upload. 
Lastly, the direct link to the uploaded image will be copied to your clipboard, ready for your pasting needs.  

## Errors to be addressed:
I checked some basic exceptions, but there is still an error where the watchdog library gets a different time stamp for the screen shot than the actual file by several seconds. I believe this is because watch dog is not perfectly precise in detecting file creation or file modification time. But I could potentially just revamp the file dialogue window interaction to choose the most recently created item(s) in the screenshots directory with the "Screenshot" string in its name. 

Additionally the elements' css selectors on imgur could change overtime so I will make sure to update the css selectors as needed. I could use xpath too for the interaction with the web page but it usually didn't work for the more complex css items which are either activated by hovering only, or which appear intermittently depending on successful upload.

### Note
If you want to change the screenshot directory which the app uses after you already entered it, simply delete the pickle file in the same directory as your script.
If you want to change your default screenshot directory on Mac OSX, follow the instructions here: https://www.hellotech.com/guide/for/how-to-change-where-screenshots-are-saved-on-mac

Unfortunately, this script is only available on Mac OSX, but all I would need to make it windows compatible is to change the way the program interacts with the file upload dialogue window in the section which contains the osascript. Updates to follow!

Happy Auto Screenshotting!
