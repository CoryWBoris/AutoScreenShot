# AutoScreenShot.py by Cory Boris
A simple Python script for Mac OSX for uploading images to Imgur using undetected-chromedriver which uses Selenium via Chrome.

## Requirements
Python 3 (https://www.python.org/downloads/)  
The following python libraries:  
selenium, undetected-chromedriver (installs selenium if you don't have it), watchdog, certifi  
And for the web browser:  
Latest Version of Google Chrome, at least one adblocker (uBlock Origin is great!)

## Installation
For your convenience, make a folder somewhere called AutoScreenShot.  
Clone or download this repository to that folder.
Then install the required packages in terminal:   
`pip install certifi selenium undetected-chromedriver watchdog`

## Usage
### For First Time Use:
run the script in terminal: python3 AutoScreenshot.py
You will be prompted for the directory of your ad blocker. Don't panic, I will show you how to find it on mac.
First you need to know what profile has the extension. Just check in chrome by clicking the profile picture when you have the ad blocker enabled
The path will look something like this:
/Users/{your_username}/Library/Application Support/Google/Chrome/{your_profile_name}/Extensions/cjpalhdlnbpafiamejdnhcphjbkeiagm/1.49.2_0'
This is what version 1.49.2 of uBlock Origin would look like. It is a long and nasty string, but basically this is how chrome stores plugins. The good news for you is that once you set this, unless you delete the pickle file in the directory of this script, it will be saved forever. But if you update the plugin, you must change the directory for the script to run.
After entering this file path, a selenium instance of chrome will open, and then you will be prompted to enter the directory of your screenshot. 
After your enter your screenshot directory, you will see "started event handler" and you are good to go and ready for general use. 

### For General Use:
If your directory is already entered the first time, then you will just see selenium's instance of Google Chrome open and the "started event handler" message.  
When a new screenshot is added to the specified directory, the script will automatically upload it to Imgur.com/upload. On macs, after the screenshot is taken, you have to drag the image to the right after it appears in the bottom right corner for it to be immediately available in the screenshot file directory. Or you can just wait a few seconds.  
Lastly, the direct link to the uploaded image will be copied to your clipboard, ready for your pasting needs.  
Last lastly, pressing "ctrl" + "c" is the only way to quit for now.

## Errors to be addressed:
I checked for most exceptions, I'm sure I left a few out. Overall the function is robust, as I circumvented the slight imprecision of using the WatchDog library when detailing the exact creation time and date of a file, especially since Apple is interfering with a quick way to access this data, most likely for security purposes. I basically sort the screenshots by their default string, which contains the date stamp given by Apple.

Additionally the elements' css selectors on imgur could change overtime so I will make sure to update the css selectors as needed. I could use xpath too for the interaction with the web page but it usually didn't work for the more complex css items which are either activated by hovering only, or which appear intermittently depending on successful upload.

I'd like to use some other method, possibly using the web driver, to upload a given screenshot. For now I am using osascript, and it works so I am cool with it at the moment.

### Note
If you want to change the screenshot directory or the ad blocker directory which the app uses after you already entered it, simply delete the pickle file in the same directory as your script.  
If you want to change your default screenshot directory on Mac OSX, follow the instructions here: https://www.hellotech.com/guide/for/how-to-change-where-screenshots-are-saved-on-mac  
If you want to change your default screenshot filetype, in terminal write:  
`defaults write com. apple. screencapture type {enter_type_here}`  
You can choose JPG, TIFF, GIF, PDF and PNG, but only one.

Unfortunately, this script is only available on Mac OSX, but all I would need to make it windows compatible is to change the way the program interacts with the file upload dialogue window in the section which contains the osascript. Updates to follow!

Happy Auto Screenshotting!
