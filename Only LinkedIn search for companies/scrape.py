import sys, os
import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse
import time, random
import pandas as pd

def main(argv):
    chainCall(argv[0])

def googleSearch(query, head):
    g_clean = [] # this is the list we store the search results
    url = 'https://www.google.com/search?q={}&ie=utf-8&oe=utf-8'.format(query) # this is the actual query we are going to scrape
    header0 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "en-US,en;q=0.9", 
        "Dnt": "1",
        "Referer": "https://www.google.com/",
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }

    header1 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "en-US,en;q=0.5", 
        "Dnt": "1",
        "Referer": "https://www.google.com/",
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    }

    header2 = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "en-us,en",
        "Referer": "https://www.google.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15"
    }

    if head == 0:
        header = header0
    elif head == 1:
        header = header1
    else:
        header = header2
                
    try:
        html = requests.get(url)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'lxml')
            a = soup.find_all('a') # a is a list
            for i in a:
                k = i.get('href')
                try:
                    m = re.search(r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))", k)
                    n = m.group(0)
                    rul = n.split('&')[0]
                    domain = urlparse(rul)
                    if(re.search(r".google.com|.youtube.com|.wikipedia.org|.google.ro", domain.netloc)):
                        continue
                    else:
                        g_clean.append(rul)
                except:
                    continue
    except Exception as ex:
        print(str(ex))
    finally:
        return g_clean

def chainCall(file1):
    delays =[7, 4,  6, 2, 10, 19, 13,  3, 17,  5,
            18, 6, 20, 8,  6,  3,  7, 11, 16, 19,
            12, 2, 4, 10, 11, 19,  3, 17, 18, 16,
            2,  5, 9, 12,  8,  6,  4,  7,  9,  1,
            12, 4, 11, 7, 15, 20,  9, 12, 14,  6,
            13, 5, 1,  3,  7, 18, 17, 19, 20, 13]

    df = pd.read_csv(file1)
    print(file1)
    df = df[["Website", "Company Name","Business Category","Industry","Employee Name","First Name","Last Name","Middle Name","Job Title", "Personal Email Address", "Generic Company Email Address", "Other Company Email Address", "Emails from other domains"]]
    df['LinkedIn'] = ""
    for index, row in df.iterrows():
        if row[1] != ' ' and str(row[1]) != "nan":
            print("-----------------------------" + str(row[1]))
            time.sleep(random.choice(delays))
            searchIndex = "LinkedIn " + str(row[1]) + " " + str(row[2])
            searchIndex = urllib.parse.quote_plus(searchIndex)
            web = googleSearch(searchIndex, index % 3)
            if not web:
                web.append('')
            if ("/dir" in web[0] or "pub" in web[0]) and len(web) > 1:
                web.pop(0)
                if not web:
                    web.append('')
            df.at[index, 'LinkedIn'] = web[0]
        else:
            df = df.drop(index)
    df.to_csv(file1[:-4] +"_Modified.csv", index=False)

if __name__ == "__main__":
    main(sys.argv[1:])