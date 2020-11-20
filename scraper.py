import requests
import re
from bs4 import BeautifulSoup
from scapy.all import *
import csv
import html5lib
import time

searchString = '(intitle:"modeling" OR intitle:"modelling" OR intitle:"model based" OR intitle:"model driven") AND (intitle:"multi*" OR intitle:"blended") AND (intitle:"notation*" OR intitle:"syntax*" OR "intitle:editor" OR "intitle:tool" OR "intitle:software")'

proxies = {
  'http': '161.202.226.194:8123',
  'https': '161.202.226.194:8123'
}

def getURL(startPageNumber):
    return 'https://scholar.google.be/scholar?start={startPageNumber}&q={searchString}'.format(startPageNumber = startPageNumber, searchString = searchString)

with open('publications.csv', mode='w', newline='', encoding='utf-8') as publications_file:
    pub_writer = csv.writer(publications_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    pub_writer.writerow(['Authors', 'Title', 'Year', 'Publisher', 'Link'])

    for pageNum in range(510, 680, 10):
    #for pageNum in range(0, 10, 10):
        time.sleep(2)
        page = requests.get(getURL(pageNum))
        #page = requests.get('https://httpbin.org/ip', proxies=proxies)
        print(page)
        
        soup = BeautifulSoup(page.content, 'html.parser')
        print('hello')
    
        #soup = BeautifulSoup(open("scholar.html"), "html5lib", from_encoding='utf-8')

        hits = soup.find_all('div', class_='gs_ri')
        
        title = ''
        link = ''
        pubAuthors = ''
        publisher = ''
        year = ''
        
        for hit in hits:
            titleElement = hit.find_all('h3', class_='gs_rt')[0]
            
            title = titleElement.text
            print(title)
            ahref = titleElement.find('a')
            if ahref is not None:
                link = ahref.get('href')
            
            authorsList = hit.find_all('div', class_='gs_a')
            if authorsList is not None:
                authors = authorsList[0].text.split('-')[0].strip()
                print(authors)
                lastAuthorListChar = authors.encode('utf-8')[-1]
                if lastAuthorListChar==166:
                    pubAuthors = '{0}, et al.'.format(authors[:-3])
                else:
                    pubAuthors = '{0}'.format(authors)
                print(len(authorsList[0].text.split('-')))
                if len(authorsList[0].text.split('-'))>1:
                    publisher = authorsList[0].text.split('-')[-1].strip()
                if len(authorsList[0].text.split('-'))>2:
                    year = authorsList[0].text.split('-')[-2].strip().split(',')[-1].strip()
            
            pub_writer.writerow([pubAuthors, title, year, publisher, link])