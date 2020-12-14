from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
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
        self.driver = self.load_chromedriver(BlinkParser.CHROME_PATH)
        
    def load_chromedriver(self, path):
        chrome_options = Options()
        chrome_options.page_load_strategy = 'eager'
        return webdriver.Chrome(path, options=chrome_options)
    
    def parse(self):
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
                        'title': branch.find_element_by_class_name('Teaser-title').text,
                        'street': branch.find_element_by_class_name('Teaser-address').text,
                        'phone': branch.find_element_by_class_name('Teaser-phone').text,
                        'url': branch.find_element_by_class_name('Teaser-titleLink').get_attribute('href')}
                    
                    self.branch_info.append(temp_branch)
    
    # def parse_status(self):
    #     updated_statuses = []
        
    #     # HELPER: returns status as integer value for efficient storage and comparison
        # def get_status_code(status):    
        #     for status_code, status_text_list in BlinkParser.branch_status_dict.items():
        #         if status in status_text_list:
        #             print(status_code, status_text_list)
        #             return status_code
        #     return None
        
    #     # TODO: remove repetitive directory parsing code 
    #     for url in self.branch_directory_urls:
    #         self.driver.get(url)
    
    #         # parse elements containing individual branch information
    #         wait = WebDriverWait(self.driver, 10)
    #         cities = wait.until(lambda d: d.find_elements_by_class_name('Directory-cityContainer'))
            
    #         for city in cities:
    #             branches = city.find_elements_by_class_name('Directory-listTeaser')
                
    #             for branch in branches:
    #                 # text is located in different div depending on branch status
    #                 try:
    #                     status = branch.find_element_by_class_name('Hours-statusText').text.strip()
    #                 except:
    #                     status = branch.find_element_by_class_name('Teaser-text').text.strip()
                        
    #                 branch_title = branch.find_element_by_class_name('Teaser-title').text,
    #                 branch_status = get_status_code(status)
                    
    #                 updated_statuses.append(branch_title, branch_status)
                    
    #     return updated_statuses

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
        
        # TODO: remove hardcoded urls 
        urls = ['https://locations.blinkfitness.com/ca/california/6714-pacific-boulevard', 'https://locations.blinkfitness.com/ca/california/15519-normandie-avenue', 'https://locations.blinkfitness.com/ca/california/2251-west-ball-road', 'https://locations.blinkfitness.com/ca/california/1060-west-alameda-avenue', 'https://locations.blinkfitness.com/ca/california/2450-east-century-blvd', 'https://locations.blinkfitness.com/ca/california/1205-1299-w-foothill-blvd', 'https://locations.blinkfitness.com/ca/california/130-west-g-street', 'https://locations.blinkfitness.com/ca/california/16121-bellflower-blvd.', 'https://locations.blinkfitness.com/fl/jacksonville/1102-dunn-avenue', 'https://locations.blinkfitness.com/fl/miramar/3352-south-university-drive', 'https://locations.blinkfitness.com/il/chicago/5160-south-pulaski-road', 'https://locations.blinkfitness.com/il/chicago/3243-west-115th-street', 'https://locations.blinkfitness.com/il/chicago/3145-south-ashland-avenue', 'https://locations.blinkfitness.com/il/chicago/7509-west-cermak-road', 'https://locations.blinkfitness.com/il/chicago/8749-s.-ridgeland-avenue', 'https://locations.blinkfitness.com/il/chicago/1926-demptser-st', 'https://locations.blinkfitness.com/ma/beverly/71-dodge-street', 'https://locations.blinkfitness.com/ma/medford/465-salem-street', 'https://locations.blinkfitness.com/mi/redford/9395-telegraph-road', 'https://locations.blinkfitness.com/mi/warren/26475-hoover-road', 'https://locations.blinkfitness.com/nj/new-jersey/151-bergen-town-center', 'https://locations.blinkfitness.com/nj/new-jersey/4-memorial-drive', 'https://locations.blinkfitness.com/nj/new-jersey/35-journal-square', 'https://locations.blinkfitness.com/nj/new-jersey/3053-route-46', 'https://locations.blinkfitness.com/nj/new-jersey/2700-route-22', 'https://locations.blinkfitness.com/nj/new-jersey/1006-route-46', 'https://locations.blinkfitness.com/nj/new-jersey/1701-west-edgar-road', 'https://locations.blinkfitness.com/nj/new-jersey/451-valley-street', 'https://locations.blinkfitness.com/nj/new-jersey/440-eastern-parkway', 'https://locations.blinkfitness.com/nj/new-jersey/663-main-avenue', 'https://locations.blinkfitness.com/nj/new-jersey/133-new-brunswick-avenue', 'https://locations.blinkfitness.com/nj/new-jersey/600-central-avenue', 'https://locations.blinkfitness.com/nj/new-jersey/235-255-east-front-street', 'https://locations.blinkfitness.com/nj/new-jersey/2-14-ferry-street', 'https://locations.blinkfitness.com/nj/new-jersey/364-centre-street', 'https://locations.blinkfitness.com/nj/philadelphia/498-beverly-rancocas-road', 'https://locations.blinkfitness.com/ny/bronx/1380-metropolitan-avenue', 'https://locations.blinkfitness.com/ny/bronx/744-st.-anns-avenue', 'https://locations.blinkfitness.com/ny/bronx/820-concourse-village-west', 'https://locations.blinkfitness.com/ny/bronx/2374-grand-concourse', 'https://locations.blinkfitness.com/ny/bronx/3580-white-plains-road', 'https://locations.blinkfitness.com/ny/bronx/1490-macombs-road', 'https://locations.blinkfitness.com/ny/bronx/5520-broadway', 'https://locations.blinkfitness.com/ny/bronx/570-melrose-avenue', 'https://locations.blinkfitness.com/ny/bronx/932-southern-boulevard', 'https://locations.blinkfitness.com/ny/bronx/645-e.-tremont-avenue', 'https://locations.blinkfitness.com/ny/bronx/1421-webster-ave', 'https://locations.blinkfitness.com/ny/bronx/3000-jerome-avenue', 'https://locations.blinkfitness.com/ny/brooklyn/2166-nostrand-avenue', 'https://locations.blinkfitness.com/ny/brooklyn/833-flatbush-avenue', 'https://locations.blinkfitness.com/ny/brooklyn/250-utica-avenue', 'https://locations.blinkfitness.com/ny/brooklyn/3779-nostrand-avenue', 'https://locations.blinkfitness.com/ny/brooklyn/1002-gates-avenue', 'https://locations.blinkfitness.com/ny/brooklyn/1413-fulton-street', 'https://locations.blinkfitness.com/ny/brooklyn/252-atlantic-avenue', 'https://locations.blinkfitness.com/ny/brooklyn/9029-flatlands-avenue', 'https://locations.blinkfitness.com/ny/brooklyn/2857-w.-8th-street', 'https://locations.blinkfitness.com/ny/brooklyn/399-knickerbocker-avenue', 'https://locations.blinkfitness.com/ny/brooklyn/227-fourth-avenue', 'https://locations.blinkfitness.com/ny/brooklyn/287-broadway', 'https://locations.blinkfitness.com/ny/brooklyn/5109-fourth-avenue', 'https://locations.blinkfitness.com/ny/brooklyn/81-83-east-98th-street', 'https://locations.blinkfitness.com/ny/brooklyn/1134-fulton-st.', 'https://locations.blinkfitness.com/ny/long-island/121-broadhollow-road', 'https://locations.blinkfitness.com/ny/long-island/1790-veterans-memorial-highway', 'https://locations.blinkfitness.com/ny/long-island/175-sunrise-highway', 'https://locations.blinkfitness.com/ny/long-island/480-suffolk-avenue', 'https://locations.blinkfitness.com/ny/long-island/1789-grand-avenue', 'https://locations.blinkfitness.com/ny/long-island/14-brooklyn-avenue', 'https://locations.blinkfitness.com/ny/long-island/358-n.-broadway-mall', 'https://locations.blinkfitness.com/ny/long-island/600-north-wellwood-avenue', 'https://locations.blinkfitness.com/ny/long-island/450-main-street', 'https://locations.blinkfitness.com/ny/manhattan/16-e.-4th-street', 'https://locations.blinkfitness.com/ny/manhattan/4200-broadway', 'https://locations.blinkfitness.com/ny/manhattan/301-w.-125th-street', 'https://locations.blinkfitness.com/ny/manhattan/600-third-avenue', 'https://locations.blinkfitness.com/ny/manhattan/27-w.-116th-street', 'https://locations.blinkfitness.com/ny/manhattan/308-eighth-avenue', 'https://locations.blinkfitness.com/ny/manhattan/127-w.-30th-street', 'https://locations.blinkfitness.com/ny/manhattan/5-bryant-park', 'https://locations.blinkfitness.com/ny/manhattan/111-nassau-street', 'https://locations.blinkfitness.com/ny/manhattan/240-e.-54th-street', 'https://locations.blinkfitness.com/ny/manhattan/125-park-avenue', 'https://locations.blinkfitness.com/ny/manhattan/98-avenue-a', 'https://locations.blinkfitness.com/ny/queens/163-02-jamaica-avenue', 'https://locations.blinkfitness.com/ny/queens/32-27-steinway-street', 'https://locations.blinkfitness.com/ny/queens/78-14-roosevelt-avenue', 'https://locations.blinkfitness.com/ny/queens/102-16-liberty-avenue', 'https://locations.blinkfitness.com/ny/queens/56-02-roosevelt-avenue', 'https://locations.blinkfitness.com/ny/queens/108-14-roosevelt-avenue', 'https://locations.blinkfitness.com/ny/queens/130-20-farmers-blvd', 'https://locations.blinkfitness.com/ny/queens/55-27-myrtle-avenue', 'https://locations.blinkfitness.com/ny/queens/220-05-hillside-avenue', 'https://locations.blinkfitness.com/ny/upstate-new-york/4979-w.-taft-road', 'https://locations.blinkfitness.com/ny/upstate-new-york/4722-onondaga-blvd', 'https://locations.blinkfitness.com/ny/upstate-new-york/2833-w-ridge-rd', 'https://locations.blinkfitness.com/ny/westchester/8000-mall-walk', 'https://locations.blinkfitness.com/ny/westchester/100-main-street', 'https://locations.blinkfitness.com/pa/philadelphia/8914-frankford-avenue', 'https://locations.blinkfitness.com/pa/philadelphia/5597-tulip-street', 'https://locations.blinkfitness.com/pa/philadelphia/330-w.-oregon-avenue', 'https://locations.blinkfitness.com/tx/dallas-fort-worth/3529-heritage-trace-pkwy', 'https://locations.blinkfitness.com/tx/dallas-fort-worth/7901-mid-cities-blvd', 'https://locations.blinkfitness.com/tx/dallas-fort-worth/7410-n-beach-st', 'https://locations.blinkfitness.com/tx/dallas-fort-worth/615-harwood-rd', 'https://locations.blinkfitness.com/tx/houston/4400-north-freeway', 'https://locations.blinkfitness.com/tx/houston/7840-long-point-rd', 'https://locations.blinkfitness.com/tx/houston/11145-westheimer-road', 'https://locations.blinkfitness.com/tx/houston/8201-broadway-street']
        #urls = self.get_urls()
        
        for url in urls:
            status_code = self.get_status_code(url)
            title = self.driver.find_element_by_class_name('LocationName-geo').text
            #current_time = time.localtime(time.time()) # TODO: check how to store datetime in database
            
            if not status_code:
                capacity = self.driver.find_element_by_class_name('Core-capacityStatus').text
            else:
                capacity = None
                
            if capacity:
                print(title, status_code, capacity)
                
        self.driver.quit()
            
if __name__ == '__main__':
    parser = BlinkParser()
    #parser.parse()
    parser.parse_capacity()
    
    