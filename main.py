from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import urllib2, json, datetime, pytz



fg = FeedGenerator()

def createRSS():
    fg.title('Decommissioned Street Sign Feed')
    fg.link( href='http://ottawa.ca/en/residents/transportation-and-parking/traffic/decommissioned-street-name-signs')
    fg.subtitle('Lets you know when signs are posted.')
    fg.language('en')
    rssfeed = fg.rss_str(pretty=True)

def addToFeed(Signs):
    for sign in Signs:
        fe = fg.add_entry()
        fe.title(sign + ' Posted')
        
        #Get local time and add UTC information.
        local_system_time = datetime.datetime.utcnow()
        local_system_utc = pytz.utc.localize(local_system_time)

        fe.pubdate(local_system_utc)
    fg.rss_file('rss.xml')
    #fg.atom_file('atom.xml') #Still a bug here :(

def updateFeed():
    feed = BeautifulSoup(open('rss.xml'))
    #Get the information from the previous feed.
    print feed.find('title').getText()
    print feed.link.nextSibling
    print feed.find('description').getText()


def exportFeed():
    fg.rss_file('rss.xml')


def getNew(Signs):
    #Read in previously saved JSON file containing serialized Dict of Signs
    json_file = open('signs.json')
    json_str = json_file.read()

    json_data = json.loads(json_str.encode('ascii','ignore').translate(None, '\n\t\r\u'))

    newSigns = {}
    for i in Signs:
        if i not in json_data:
            newSigns[i] = Signs[i]
    return newSigns

def exportToJSON(Signs):
    with open('signs.json', 'w+') as fileOpen:
        json.dump(Signs, fileOpen)

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
    return Signs


def main():


    Signs = getSigns()
    #updateFeed()
    createRSS()
    addToFeed(Signs)
    #exportFeed()
    #createRSS()
    #exportToFeed(Signs)



if __name__ == "__main__":
    main()
