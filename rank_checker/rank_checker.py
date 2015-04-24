from bs4 import BeautifulSoup
import requests
import time
import random

pages_deep = 1 # production would be more like 100 pages deep

# from: http://techblog.willshouse.com/2012/01/03/most-common-user-agents/
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9) AppleWebKit/537.71 (KHTML, like Gecko) Version/7.0 Safari/537.71',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
]

# from http://www.bigbossmas.com/web-development/list-of-mobile-device-sizes/
# added these as they will eventually be running side by side for both desktop and mobile updates
MOBILE_USER_AGENTS = [
    'Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; Sensation_4G Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Safari/533.16',
    'Mozilla/5.0 (Java 1.6.0_01; Windows XP 5.1 x86; en) ICEbrowser/v6_1_2',
    'Mozilla/5.0 (Linux; Android 4.0.3; GT-N7000 Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
    'Mozilla/5.0 (Linux; Android 4.0.3; GT-N7000 Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
    'Mozilla/5.0 (Linux; Android 4.0.3; HTC One V Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
    'Mozilla/5.0 (Linux; Android 4.0.3; HTC One V Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
    'Mozilla/5.0 (Linux; Android 4.0.3; HTC PH39100 Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
    'Mozilla/5.0 (Linux; Android 4.0.3; en-gb; GT-I5510 Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'
]

referrer = ''

def rank_checker(query):
    '''
    This is the initial rank checking script, it needs more thorough testing but initial
    tests are looking good.

    '''

    proxies = None # add optional proxy

    rank_position = 0    # keeps track of the ranking position

    for start in range(int(pages_deep)):
        '''
        Opens search result and iterates through the SERP pagination.
        Each iteration requests 10 results at a time.
        '''

        url = "http://www.google.com/search?q=" + query.replace(' ', '+') + "&start=" + str(start*10) \
         + '&num=10&pws=0&filter=0'

        if rank_position < 1:
            referrer = 'http://www.google.com'
        else:
            pass
            
        headers = {
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Encoding': 'gzip,deflate',
              'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4',
              'Cache-Control': 'no-cache',
              'Connection': 'close',
              'DNT': '1',
              'Pragma': 'no-cache',
              'Referrer' : referrer, 
              'User-Agent': random.choice(USER_AGENTS)
              }
      
        r = requests.get(url, timeout=20, headers=headers, proxies=proxies)
        data = r.text
        soup = BeautifulSoup(data)
        time.sleep(5)

        results = soup.findAll("h3", { "class" : "r" })
        for div in results:
            rank_position += 1
            print '#{}'.format(rank_position), div.find('a')['href'] # 'Ref {}'.format(referrer) - testing the referrer

        referrer = url

rank_checker(query) # query being the search result!!
