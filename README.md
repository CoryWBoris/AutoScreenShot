# AutoScreenShot
A simple Python script for uploading images to Imgur using undetected-chromedriver which uses Selenium via Chrome.

## Requirements
Python 3
Selenium
Undetected Chromedriver
Watchdog

## Installation
Clone this repository.
Install the required packages: 
pip install selenium watchdog undetected-chromedriver
Run the script: python3 AutoScreenshot.py
## Usage
Enter the directory you want to watch for new screenshot photos.
When a new image is added to the directory, the script will automatically upload it to Imgur.
The direct link to the uploaded image will be copied to your clipboard.

### Note
I haven't checked for exceptions yet, but so far I haven't experienced anything out of the ordinary. Of course the elements on imgur could change overtime so I will make sure to update the css selectors as needed.

Happy Auto Screenshotting!
