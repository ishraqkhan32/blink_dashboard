import time
from BlinkParser import BlinkParser
from app import scrape_and_store_capacities

if __name__ == "__main__":
    parser = BlinkParser()
    parser.parse()
    
    while True:
        # get starting time
        sec_start = time.time()
        
        # parse capacities + update database
        capacities = parser.parse_capacity()
        scrape_and_store_capacities(capacities)
        
        # get ending time
        time_end = time.strftime('%c', time.localtime())
        sec_end = time.time()
        
        # print summary
        duration = sec_end - sec_start
        print(f'Database updated at {time_end} - {round(duration)}s')
        
        time.sleep(800)
        
    