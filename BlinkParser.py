from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time

class BlinkParser():
    CHROME_PATH = "/Users/ik/bin/chromedriver"

    branch_status_dict = {
        0: ['Temporarily Closed', 'Closed'],
        1: ['Coming Soon'], 
        2: ['Open Now'],
        3: ['Closed - Opens at']}

    def __init__(self):
        self.driver = None
        self.branch_directory_urls = []
        self.location_info = []
        
    def parse(self):
        self.load_chromedriver(BlinkParser.CHROME_PATH)

        blink_directory_url = 'https://locations.blinkfitness.com/index.html'

        self.driver.get(blink_directory_url)
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
        
    def load_chromedriver(self, path):
        chrome_options = Options()
        chrome_options.page_load_strategy = 'eager'
        self.driver = webdriver.Chrome(path, options=chrome_options)

    def find_hrefs(self, list_a_tags, url_starts_with, url_does_not_include):
        list_urls = []

        for link in list_a_tags:
            url_string = link.get_attribute('href')

            if url_string.startswith(url_starts_with):
                if not any(x in url_string for x in url_does_not_include):
                    list_urls.append(url_string)
        return list_urls
    
    def parse_branch_info(self):
        def parse_status(branch_element):
            # text is located in different div depending on branch status
            try:
                status = branch.find_element_by_class_name('Hours-statusText').text.strip()
            except:
                status = branch.find_element_by_class_name('Teaser-text').text.strip()
            
            # return status as integer value for efficient storage and comparison
            for k,v in BlinkParser.branch_status_dict.items():
                if status in v:
                    return k
            return None
        
        for url in self.branch_directory_urls:
            self.driver.get(url)
    
            # parse elements containing individual branch information
            wait = WebDriverWait(self.driver, 10)
            cities = wait.until(lambda d: d.find_elements_by_class_name('Directory-cityContainer'))
            
            for city in cities:
                branches = city.find_elements_by_class_name('Directory-listTeaser')
                
                for branch in branches:
                    # replace assignments with database update code
                    temp_branch = {}
                    temp_branch['state'] = url[-2:].upper()
                    temp_branch['city'] = city.find_element_by_class_name('Directory-cityName').text
                    temp_branch['status'] = parse_status(branch)
                    temp_branch['url'] = branch.find_element_by_class_name('Teaser-titleLink').get_attribute('href')
                    temp_branch['title'] = branch.find_element_by_class_name('Teaser-title').text
                    temp_branch['street'] = branch.find_element_by_class_name('Teaser-address').text
                    temp_branch['phone'] = branch.find_element_by_class_name('Teaser-phone').text
                    
                    self.location_info.append(temp_branch)
        
        # TODO: develop function that takes branch URL and returns capacity 
        def parse_capacity(self, branch_url):
            # TODO: develop function that checks status
            pass