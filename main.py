from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import urllib2, json

fg = FeedGenerator()


def createRSS():
    fg.title('Decommissioned Street Sign Feed')
    fg.link( href='http://ottawa.ca/en/residents/transportation-and-parking/traffic/decommissioned-street-name-signs')
    fg.subtitle('Lets you know when signs are posted.')
    fg.language('en')
    rssfeed = fg.rss_str(pretty=True)

def exportRSS(Signs):
    for sign in Signs:
        fe = fg.add_entry()
        fe.title(sign + ' Posted')
    fg.rss_file('rss.xml')
    #fg.atom_file('atom.xml')

def getNew(Signs):
    print "empty"


def getSigns():

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

    with open('signs.json', 'w') as fileOpen:
        json.dump(Signs, fileOpen)

    return Signs


def main():

    Signs = getSigns()
    createRSS()
    exportRSS(Signs)



if __name__ == "__main__":
    main()
