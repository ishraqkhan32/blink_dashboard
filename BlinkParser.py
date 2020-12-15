from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

class BlinkParser():
    CHROME_PATH = "/Users/ik/bin/chromedriver"
    DIRECTORY_URL = 'https://locations.blinkfitness.com/index.html'
    
    branch_status_dict = {
        0: ['Open Now - Closes at'],
        1: ['Opening Soon'], 
        2: ['Temporarily Closed', 'Closed'],
        3: ['Closed - Opens at']}

    def __init__(self):
        self.driver = None
        self.branch_directory_urls = []
        self.branch_info = []
        
    def load_chromedriver(self, path):
        chrome_options = Options()
        chrome_options.page_load_strategy = 'eager'
        return webdriver.Chrome(path, options=chrome_options)
    
    def parse(self):
        self.driver = self.load_chromedriver(BlinkParser.CHROME_PATH)
        self.driver.get(BlinkParser.DIRECTORY_URL)
        wait = WebDriverWait(self.driver, 10)
    
        branch_links = wait.until(lambda d: d.find_elements_by_tag_name('a'))
        
        # not including virginia beach since VA does not have standard directory like all other states
        self.branch_directory_urls = self.find_hrefs(
            list_a_tags=branch_links,
            url_starts_with='https://locations.blinkfitness.com/',
            url_does_not_include=['index','search','virginia-beach'])
        
        # if urls not parsed yet, then sleep and retry after 1 second
        while len(self.branch_directory_urls) == 0:
            time.sleep(1)
            
        self.parse_branch_info()
        
        self.driver.quit()
  

    def find_hrefs(self, list_a_tags, url_starts_with, url_does_not_include):
        list_urls = []

        for link in list_a_tags:
            url_string = link.get_attribute('href')

            if url_string.startswith(url_starts_with):
                if not any(x in url_string for x in url_does_not_include):
                    list_urls.append(url_string)
        return list_urls        
    
    def parse_branch_info(self):
        for url in self.branch_directory_urls:
            self.driver.get(url)
    
            # parse elements containing individual branch information
            wait = WebDriverWait(self.driver, 10)
            cities = wait.until(lambda d: d.find_elements_by_class_name('Directory-cityContainer'))
            
            for city in cities:
                branches = city.find_elements_by_class_name('Directory-listTeaser')
                
                for branch in branches:
                    temp_branch = {
                        'state': url[-2:].upper(),
                        'city': city.find_element_by_class_name('Directory-cityName').text,
                        'street': branch.find_element_by_class_name('Teaser-address').text,
                        'title': branch.find_element_by_class_name('Teaser-title').text,
                        'phone': branch.find_element_by_class_name('Teaser-phone').text,
                        'url': branch.find_element_by_class_name('Teaser-titleLink').get_attribute('href')}
                    
                    self.branch_info.append(temp_branch)

    def get_urls(self):
        return [branch['url'] for _,branch in enumerate(self.branch_info)]
    
    @staticmethod
    def status_to_code(status):    
        for status_code, status_text_list in BlinkParser.branch_status_dict.items():
            if status in status_text_list:
                return status_code
        return None
     
    def get_status_code(self, url):
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 3)
        
        try:
            status = wait.until(lambda d: d.find_element_by_class_name('Hours-statusText')).text 
        except:
            # for branches that have no current status (usually branches that have not been opened yet)
            status = wait.until(lambda d: d.find_element_by_class_name('Core-openingDate')).text
    
        return BlinkParser.status_to_code(status)
        
    def parse_capacity(self):
        # load new driver in case connection refused from too many requests from initial parse
        self.driver = self.load_chromedriver(BlinkParser.CHROME_PATH)
        
        urls = self.get_urls()
        capacities = []
        
        for url in urls:
            status_code = self.get_status_code(url)
            
            # status code corresponds to dictionary at beginning of class (0 = branch is open)
            # find_elements used with walrus operator to avoid error for certain webpages where Core-capacityStatus shows up for unopened branches (it shouldn't)
            if not status_code and len(cap_element := self.driver.find_elements_by_class_name('Core-capacityStatus')) > 0:
                capacity = cap_element[0].text
            else:
                capacity = None
            
            capacities.append({
                'title': self.driver.find_element_by_class_name('LocationName-geo').text,
                'timestamp': datetime.now(),
                'status_code': status_code,
                'capacity': capacity 
            })
            
        self.driver.quit()
        return capacities
