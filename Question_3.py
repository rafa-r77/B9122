# -*- coding: utf-8 -*-
"""
web_crawler_stack.py
    - The web crawler with a stack.
@author: Dongwook Shin and Yash Kanoria, 2014/08/14
@author: Kriste Krstovski, 2018/08/20 (edits to reflect Python 3 version)
This web crawler walks through the URLs in the source website and keep
crawling until there is no URL to be scanned. It stops crawling if a preset
maximum number of urls have been visited.

"""
from bs4 import BeautifulSoup
import re, urllib.parse, urllib.request
import numpy as np

url = "http://www8.gsb.columbia.edu"

urls = [url]    #queue of urls to crawl
seen = [url] # stack of urls seen so far
opened = []
score_URL = [1]

maxNumUrl = 50;
print("Starting with url="+str(urls))
while len(urls) > 0 and len(opened) < maxNumUrl:
    # DEQUEUE A URL FROM urls AND TRY TO OPEN AND READ IT
    try:
        curr_url=urls.pop(0)
        #print("num. of URLs in stack: %d " % len(urls))
        webpage=urllib.request.urlopen(curr_url)
        opened.append(curr_url)

    except Exception as ex: #if urlopen() fails
        print(ex)
        continue    #skip code below

    # IF URL OPENS, CHECK WHICH URLS THE PAGE CONTAINS
    
    # ADD THE URLS FOUND TO THE QUEUE url AND seen
    soup = BeautifulSoup(webpage, "html5lib")  #creates object soup
    
    #assign text body to another variable to count words 
    htmltext=str(soup)
    
    #lowercase the body text to get all possible matches 
    htmltext=htmltext.lower()
    
    #count occurences of keywords given
    score=htmltext.count("research")+htmltext.count("finance")+htmltext.count("engineering")+htmltext.count("business")
    
    # Put child URLs into the stack
    for tag in soup.find_all('a', href = True): #find tags with links
        childUrl = tag['href']          #extract just the link
        original_childurl = childUrl
        childUrl = urllib.parse.urljoin(url, childUrl)
        #print("url=" + url)
        #print("original_childurl=" + original_childurl)
        #print("childurl=" + childUrl)
        #print("url in childUrl=" + str(url in childUrl))
        #print("childUrl not in seen=" + str(childUrl not in seen))
        if url in childUrl and childUrl not in seen:
            #print("***urls.append and seen.append***")
            urls.append(childUrl)
            seen.append(childUrl)
            score_URL.append(score)
        else:
            print("######")

print("num. of URLs seen = %d, and opened = %d" % (len(seen), len(opened)))

#print("List of seen URLs:")
#for seen_url in seen:
  #  print(seen_url)
  
#make dictionary of URLS seen and score

dictionary=dict(zip(seen, score_URL))


from collections import OrderedDict
sorted_d = OrderedDict(sorted(dictionary.items(), key=lambda x: x[1],reverse=True))
sorted_l=list(sorted_d.items())

print("The top 25 scoring URLs seen are:")
for i in range(0,24):
    print(sorted_l[i])
