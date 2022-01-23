#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author: Shuyue Jia
@Date: Jan 22, 2022
"""

# import necessary packages
import io
import os
import sys
import re
import time
import random
from random import randint
import urllib3
import requests
import numpy as np
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import xml

from scihub import SciHub


def headers():
    """Generate a header
    """
    # A fake device to avoid the Anti reptile
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
    
    # constants
    HEADERS = {'User-Agent': USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)]}
    
    return HEADERS
    
    
def arXiv_paper_download(url, title, save_path):
    """Download papers from the arXiv
    """
    HEADERS = headers()
    try:
        with open(save_path + title + '.pdf', 'wb') as file:
            r = requests.get(url, stream=True, timeout=None, headers=HEADERS)
            
            for i in r.iter_content(2048):
                file.write(i)
        
        if osp.getsize(save_filepath) >= 10 * 1024:
            print('INFO: (From arXiv Source): Successfully downloaded this paper named as %s.pdf (Identifier: %s) !' % (title, url))
            return True
    
    except Exception as e:
        print(e)
    return False


def getHtml(url):
    HEADERS = headers()
    try:
        response = requests.get(url, timeout=None, headers=HEADERS)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        
        return response.text
    except:
        import traceback
        traceback.print_exc()


def IEEE_Download(url, title, save_path):
    """Download IEEE papers
    """
    HEADERS = headers()
    try:
        soup = BeautifulSoup(getHtml(url), 'html.parser')
        result = soup.body.find_all('iframe')
        
        downloadUrl = result[-1].attrs['src'].split('?')[0]
        response = requests.get(downloadUrl, timeout=None, headers=HEADERS)
            
        with open(save_path + title + '.pdf', 'ab+') as f:
            f.write(response.content)
        
        print('INFO: (From IEEE Source): Successfully downloaded this paper named as %s.pdf (Identifier: %s) !' % (title, downloadUrl))
        
    except:
        import traceback
        with open('errorLog','ab+') as f:
            traceback.print_exc(file=f)


def get_file_from_url(url_file, title, save_path):
    """Download PDF File from the URL directly
    """
    HEADERS = headers()
    req = requests.get(url_file, headers=HEADERS)
    bytes_io = io.BytesIO(req.content)
    
    with open(save_path + title + '.pdf', 'wb') as file:
        file.write(bytes_io.getvalue())
        time.sleep(10)
    
    print('INFO: (From Source): Successfully downloaded this paper named as %s.pdf (Identifier: %s) !' % (title, url_file))
    

def read_url(url, driver_path, page):
    """
    Read the website and return the contents of the website
    :param url: The url of the website
    :param driver_path: The path of the Google Chrome Driver
    :param page: the i-th page
    :return contents: The contents of the website
    :return driver: Chrome Driver
    """
    start_time = time.time()
    
    option = webdriver.ChromeOptions()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    # driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(driver_path, options=option)
    driver.get(url)
    
    time.sleep(5)
    contents = driver.page_source
    
    end_time = time.time()
    print('Time used for get the %d page was %7f' % (page, end_time - start_time))
    
    return contents, driver


def get_paper_title_with_link(contents):
    """
    Get the paper title on the k-th page
    """
    titles = []
    links = []
    
    # Find the citations contents
    query = 'Search within citing articles'
    query_loc = contents.find(query)
    query_cont = contents[query_loc:]
    
    # Find the paper title
    title_query = 'data-clk-atid="'
    link_query = '"><h3 class'
    
    current_title_cont = str(query_cont)
    current_link_cont = str(query_cont)
    while title_query in current_title_cont:
        # Get the paper title
        title_loc = current_title_cont.find(title_query) + len(title_query)
        current_title_cont = current_title_cont[title_loc:]
        
        if '"><span class="gs_ctg2">[' not in current_title_cont[:50]:
            title_start = current_title_cont.find('">') + len('">')
            title_end = current_title_cont.find('</a></h3>')
            paper_title = current_title_cont[title_start:title_end]
            
            if 'Web of Science' not in paper_title:
                titles.append(paper_title)
            
            # Get the paper link
            link_loc = current_link_cont.find(link_query) + len(link_query)
            current_link_cont = current_link_cont[link_loc:]
            
            link_start = current_link_cont.find('href="') + len('href="')
            link_end = current_link_cont.find('" data-')
            link = current_link_cont[link_start:link_end]
            
            # iop
            # https://iopscience.iop.org/article/10.1088/1741-2552/ac463a/meta
            # https://iopscience.iop.org/article/10.1088/1741-2552/ac463a/pdf
            if 'iopscience' in link:
                link = link.replace('meta', 'pdf')
            
            # arXiv
            # https://arxiv.org/abs/2102.04456
            # https://arxiv.org/pdf/2102.04456.pdf
            if 'arxiv' in link:
                link = link.replace('abs', 'pdf')
                link = link + '.pdf'
            
            # hindawi 
            # https://www.hindawi.com/journals/complexity/2021/6061939/
            # https://downloads.hindawi.com/journals/complexity/2021/6061939.pdf
            # https://downloads.hindawi.com/journals/jece/2021/9472053.pdf
            # https://www.hindawi.com/journals/jece/2021/9472053/
            if 'hindawi' in link and 'pdf' not in link:
                temp_loc = link.find('journals/') + len('journals/')
                temp_cont = link[temp_loc:-1]
                link = 'https://downloads.hindawi.com/journals/' + temp_cont + '.pdf'
            
            # https://www.mdpi.com/2624-6120/2/3/24/pdf
            # https://www.mdpi.com/2624-6120/2/3/24/pdf
            
            # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7522466/pdf/fnhum-14-00338.pdf
            # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7522466/
            
            links.append(link)
        
            print(paper_title)
            print(link)
            print('\n')
    
    return titles, links


# The main function
if __name__ == "__main__":
    # The path of the Chrome Driver
    driver_path = '/Users/shuyuej/.wdm/drivers/chromedriver/mac64/96.0.4664.45/chromedriver'
    
    # Citation Path
    citation_url_start = 'https://scholar.google.com/scholar?start='
    citation_url_end = '&hl=en&as_sdt=2005&sciodt=2006&cites=11369454297155265335&scipsc='
    num_citation = 36
    
    num_pages = int(num_citation / 10) + 1
    
    # Iterate each pages and get the contents
    citation_paper_titles = []
    citation_paper_links = []
    
    for index in range(num_pages):
        start = 10 * index
        citation_url = citation_url_start + str(start) + citation_url_end
        
        # Get the contents of the webpage
        contents, driver = read_url(url=citation_url, driver_path=driver_path, page=index)
        titles, links = get_paper_title_with_link(contents)
        print('Number of links: %d, and number of titles: %d' % (len(links), len(titles)))
        print('\n\n')
        
#       for i in titles:
#           citation_paper_titles.append(i)
#       
#       for i in links:
#           citation_paper_links.append(i)
#   
#   # Download all the papers via Sci-Hub 
#   sh = SciHub()
#   
#   # In default, the papers would be downloaded in the `SAVE_PATH`
#   SAVE_PATH = './Downloaded_Citations/'
#   if not os.path.exists(SAVE_PATH):
#       os.mkdir(SAVE_PATH)
#   
#   # Start to download the papers from the Sci-hub
#   print('\n\n\n', '----------Start to download papers from the Sci-hub!----------')
#   print('Getting %d paper links' % len(citation_paper_links))
#   paper_cannot_download = []
#   for i in range(len(citation_paper_links)):
#       
#       # identifier can be link URL, DOI, or PMID
#       identifier = str(citation_paper_links[i])
#       title = str(citation_paper_titles[i])
#       
#       try:
#           print('\nTry to download this paper: ', identifier)
#           
#           # Research Gate, mdpi, iopscience
#           if 'researchgate' in identifier or ('mdpi' in identifier and 'pdf' in identifier) or 'iopscience' in identifier:
#               get_file_from_url(identifier, title, SAVE_PATH)
#               try:
#                   # PDF Saved Path - You should change this to your own path
#                   sh.download(identifier=identifier, title=title, path=SAVE_PATH)
#               except:
#                   print('')
#           
#           # arXiv
#           elif 'arxiv' in identifier:
#               arXiv_paper_download(identifier, title, SAVE_PATH)
#           
#           # IEEE
#           elif 'ieee' in identifier:
#               IEEE_Download(identifier, title, SAVE_PATH)
#               try:
#                   # PDF Saved Path - You should change this to your own path
#                   sh.download(identifier=identifier, title=title, path=SAVE_PATH)
#               except:
#                   print('')
#           
#           # Others downloaded from the Sci-Hub
#           else:
#               # PDF Saved Path - You should change this to your own path
#               sh.download(identifier=identifier, title=title, path=SAVE_PATH)
#       
#       except:
#           paper_cannot_download.append(identifier)
#   
#   paper_cannot_download = np.reshape(np.array(paper_cannot_download), [-1, 1])
#   print('\n\n\nThere papers cannot be downloaded since there is no resource available at Sci-Hub! Please download these manually!')
#   print(paper_cannot_download)
    driver.close()
    driver.quit()
    