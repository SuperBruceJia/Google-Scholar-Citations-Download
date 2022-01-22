#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author: Shuyue Jia
@Date: Jan 21, 2022
"""

# import necessary packages
import os
import requests
import time
import numpy as np
import sys
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import xml
import pandas as pd
import urllib3
from random import randint

from scihub import SciHub


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
#   input('input anything\n')
    contents = driver.page_source
    
    end_time = time.time()
    print('Time used for get the %d page was %7f' % (page, end_time - start_time))

    return contents, driver


def get_paper_title(contents):
    """
    Get the paper title on the k-th page
    """
    titles = []
    
    # Find the citations contents
    query = 'Search within citing articles'
    query_loc = contents.find(query)
    query_cont = contents[query_loc:]
    
    # Find the paper title
    title_query = 'data-clk-atid="'
    
    current_cont = str(query_cont)
    while title_query in current_cont:
        current_loc = current_cont.find(title_query) + len(title_query)
        current_cont = current_cont[current_loc:]
        
        if '"><span class="gs_ctg2">[' not in current_cont[:50]:
            title_start = current_cont.find('">') + len('">')
            title_end = current_cont.find('</a></h3>')
            paper_title = current_cont[title_start:title_end]
            
            if 'Web of Science' not in paper_title:
                titles.append(paper_title)
                print(paper_title)
    
    return titles


def get_paper_link(contents):
    """
    Get the paper link on the k-th page
    """
    links = []
    
    # Find the citations contents
    query = 'Search within citing articles'
    query_loc = contents.find(query)
    query_cont = contents[query_loc:]
    
    # Find the paper link
    href = 'href='
    href_cont = str(query_cont)
    
    # Iterate to get all the paper links
    last_paper_link = ''
    temp_index = 1
    
    while href in href_cont:
        href_loc = href_cont.find(href) + len(href)
        href_cont = href_cont[href_loc:]
        
        if temp_index % 2 != 0:
            if href_cont[:5] == '"http' and href_cont[:15] != '"http://gateway' and href_cont[:16] != '"https://scholar' and href_cont[:15] != '"http://scholar':
            
                link_start = href_cont.find('"') + len('"')
                link_end = href_cont.find('data-clk') - len('" ')
                paper_link = href_cont[link_start:link_end]
                
                if paper_link != last_paper_link and 'abstract' not in paper_link and paper_link not in last_paper_link and '/abs/' not in paper_link:
                    last_paper_link = str(paper_link) 
                    links.append(paper_link)
                    print(paper_link)
                
        temp_index += 1
            
                
    return links


# The main function
if __name__ == "__main__":
    # The path of the Chrome Driver
    driver_path = '/Users/shuyuej/.wdm/drivers/chromedriver/mac64/96.0.4664.45/chromedriver'
    
    # Citation Path
    citation_url_start = 'https://scholar.google.com/scholar?start='
    citation_url_end = '&hl=en&as_sdt=2005&sciodt=2006&cites=17910156571874886383&scipsc='
    num_citation = 208
    num_pages = int(num_citation / 10) + 1
    
    # Iterate each pages and get the contents
    citation_paper_titles = []
    citation_paper_links = []
    
    for index in range(num_pages):
        start = 10 * index
        citation_url = citation_url_start + str(start) + citation_url_end
        
        # Get the contents of the webpage
        contents, driver = read_url(url=citation_url, driver_path=driver_path, page=index)
        links = get_paper_link(contents)
        titles = get_paper_title(contents)
        
        for i in titles:
            citation_paper_titles.append(i)
        
        for i in links:
            citation_paper_links.append(i)
    
    citation_paper_titles = np.reshape(np.array(citation_paper_titles), [-1, 1])
    citation_paper_links = np.reshape(np.array(citation_paper_links), [-1, 1])
    
#   print('citation_paper_titles: ', np.shape(citation_paper_titles))
#   print('citation_paper_links: ', np.shape(citation_paper_links))
    
    # Download all the papers via Sci-Hub 
    sh = SciHub()
    
    # In default, the papers would be downloaded in the `SAVE_PATH`
    SAVE_PATH = './Downloaded_Citations/'
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
        
    for paper_link in citation_paper_links:
        # identifier can be link URL, DOI, or PMID
        identifier = str(paper_link)
        
        # PDF Saved Path - You should change this to your own path
        sh.download(identifier=identifier, path=SAVE_PATH)
        print('\n')
    
    driver.close()
    driver.quit()
    
