from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import urllib2, json


def exportToRSS(updates):
    for sign in updates:
        fg = FeedGenerator()
        fg.title(sign + ' Posted')
        fg.link( href='http://ottawa.ca/en/residents/transportation-and-parking/traffic/decommissioned-street-name-signs')
        fg.subtitle('A new decommissioned street sign has been posted in Ottawa.')
        fg.language('en')
        rssfeed = fg.rss_str(pretty=True)
        fg.rss_file('rss.xml')


def main():
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
    del Signs['Street Name']

    exportToRSS(Signs)




if __name__ == "__main__":
    main()
