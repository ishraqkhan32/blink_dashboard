from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

CHROME_PATH = "/Users/ik/bin/chromedriver"
baseURL = "https://www.blinkfitness.com/locations/"
branch = "jamaica" #hard-coded for now
URL = baseURL + branch

# initialize web driver with eager page loading strategy
chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(CHROME_PATH, options=chrome_options)
driver.get(URL)

