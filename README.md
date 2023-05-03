# AutoScreenShot
A simple Python script for Mac OSX for uploading images to Imgur using undetected-chromedriver which uses Selenium via Chrome.

## Requirements
Python 3  
Selenium  
Undetected Chromedriver  
Watchdog  

## Installation
Clone this repository.
Install the required packages: 
pip install selenium watchdog undetected-chromedriver

## Usage
For first time use, run the script in terminal: python3 AutoScreenshot.py  
A selenium instance of chrome will open, and then you will be prompted to enter the directory of your screenshot. 
After your enter your directory, you will see "started event handler" and you are good to go and ready for general use.  

General Use:
If your directory is already entered the first time, then you will just see selenium's instance of Google Chrome open and the same "started event handler" message. 
When a new image is added to the specified directory, the script will automatically upload it to Imgur.com/upload. 
Lastly, the direct link to the uploaded image will be copied to your clipboard, ready for your pasting needs.  

### Note
I haven't checked for major exceptions yet, but so far I haven't experienced anything out of the ordinary. Of course the elements on imgur could change overtime so I will make sure to update the css selectors as needed.

If you want to change the screenshot directory which the app uses after you already entered it, simply delete the pickle file in the same directory as your script.
If you want to change your default screenshot directory on Mac OSX, follow the instructions here:

Unfortunately, this is only available on Mac OSX, but all I would need to make it windows compatible is to change the way the program interacts with the file upload dialogue window. Updates to follow!

Happy Auto Screenshotting!
