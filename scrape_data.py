import time
from import_data import capacity
from BlinkParser import BlinkParser

if __name__ == "__main__":
    parser = BlinkParser()
    parser.parse()
    
    while True:
        # get starting time
        sec_start = time.time()
        
        # parse capacities + update database
        capacity(parser)
        
        # get ending time
        time_end = time.strftime('%c', time.localtime())
        sec_end = time.time()
        
        # print summary
        duration = sec_end - sec_start
        print(f'Database updated at {time_end} - {round(duration)}s')
        
        time.sleep(900)
        
    