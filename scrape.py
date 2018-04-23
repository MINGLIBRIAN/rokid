import time
from crawler.crawler import get_crawler

if __name__ == '__main__':
    crawler = get_crawler(init=False)
    while True:
        # print("I'm sleeping...")

        # Update the database per 30 minutes
        time.sleep(200)
        crawler.start()
