from requests_html import HTMLSession, AsyncHTMLSession
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time

URL = 'https://www.blinkfitness.com/locations'
PATH = "/Users/ishraqkhan/bin/chromedriver"
gyms = {}

options = Options()
options.page_load_strategy = 'none'

driver = webdriver.Chrome(executable_path=PATH, options=options)
driver.get(URL)
# get all Areas web element
element = WebDriverWait(driver, timeout=15).until(lambda d: d.find_element_by_xpath('//*[@id="layout-first-page"]/div/div/bw-locations/bw-location-list[2]/div'))

# facilities = driver.find_elements_by_css_selector("#layout-first-page > div > div > bw-locations > bw-location-list > div > div > div.desktop-visible > div > div > a > h3")
#print(len(facilities))

areas = element.find_elements_by_class_name('area')
print(len(areas))

# for area in all_branches: # for each webelement
#     # find and store area_header
#     location = area.text.lower()
#     if location != "":
#         print("Location: ", location)
#         # find and store facility name
#         facilities = area.find_elements_by_xpath('.//h3[@class="facility__header"]')
#         # print(facilities)
#         print("# of facilities: ", len(facilities))



print(gyms)
driver.quit()
#     # find and store facility name 
#     facilities = area.find_elements_by_class_name("area__inner")
#     for facility in facilities:
#         branch = facility.find_element_by_class_name("facility__header").text.lower()
#         print("Branch: ", branch)


# time.sleep(5)
