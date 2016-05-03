from sys import argv,exit
from bs4 import BeautifulSoup
import requests
from html.parser import HTMLParser

input = argv[1]

"""
r = requests.get(argv[1])
"""

file = open(argv[1])

data = file.read()

data = "".join(data.split('<!--'))
data = "".join(data.split('-->'))

soup = BeautifulSoup(data, "lxml")

page_type_elem = soup.find('span', {'class': '_50f6'})
print(page_type_elem.text)

desc = soup.find('div', {'class': '_42ef'})
print(desc.text)

home_town = soup.find('div', {'class': '_42ef'})
print(home_town.text)

exit(0)

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            print("Encountered a start tag:", tag, attrs)
    def handle_endtag(self, tag):
        pass
        #print("Encountered an end tag :", tag)
    def handle_data(self, data):
        pass
        #print("Encountered some data  :", data)

parser = MyHTMLParser()
parser.feed(file.read())
