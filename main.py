from bs4 import BeautifulSoup
import urllib2

response = urllib2.urlopen('http://ottawa.ca/en/residents/transportation-and-parking/traffic/decommissioned-street-name-signs')
html = response.read()

soup = BeautifulSoup(html)
tables = soup.findAll("table")


Signs = {}

for x in xrange(0,len(tables)):
    rows = tables[x].findChildren(['tr'])
    for row in rows:
        cells = row.findChildren('td')
        Signs[(cells[0].get_text().encode('ascii','ignore')).translate(None, '\n\t\r')] = (cells[1].get_text().encode('ascii','ignore')).translate(None, '\n\t\r')

print Signs
