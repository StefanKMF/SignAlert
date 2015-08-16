#!/usr/bin/python
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import urllib2, json, datetime, pytz, subprocess, os



fg = FeedGenerator()

def createRSS():
    fg.title('Decommissioned Street Sign Feed')
    fg.link( href='http://ottawa.ca/en/residents/transportation-and-parking/traffic/decommissioned-street-name-signs')
    fg.subtitle('Lets you know when signs are posted.')
    fg.language('en')
    rssfeed = fg.rss_str(pretty=True)

def exportFeed():
    fg.rss_file('rss.xml')
    #fg.atom_file('atom.xml') #Still a bug here :(

def exportToJSON(Signs):
    with open('signs.json', 'w+') as fileOpen:
        json.dump(Signs, fileOpen)
        fileOpen.close()

def exportForTwitter(newSigns):
    with open('botfood.json','w+') as fileOpen:
        json.dump(newSigns, fileOpen)
        fileOpen.close()

def getNew(Signs):
    #Read in previously saved JSON file containing serialized Dict of Signs
    with open('signs.json', 'r') as fileOpen:
        json_str = fileOpen.read()
        json_data = json.loads(json_str.encode('ascii','ignore').translate(None, '\n\t\r\u'))
        fileOpen.close()

    newSigns = {}
    for i in Signs:
        if i not in json_data:
            newSigns[i] = Signs[i]

    return newSigns

def getSigns():

    response = urllib2.urlopen('http://ottawa.ca/en/residents/transportation-and-parking/traffic/decommissioned-street-name-signs')
    html = response.read()

    soup = BeautifulSoup(html, "html.parser")
    tables = soup.findAll("table")

    Signs = {}

    for x in xrange(0,len(tables)):
        rows = tables[x].findChildren(['tr'])
        for row in rows:
            cells = row.findChildren('td')
            Signs[(cells[0].get_text().encode('ascii','ignore')).translate(None, '\n\t\r')] = (cells[1].get_text().encode('ascii','ignore')).translate(None, '\n\t\r')
    del Signs['Street Name']
    return Signs

def newToFeed(Signs):
    for sign in Signs:
        fe = fg.add_entry()
        fe.title(sign + ' Posted, ' + Signs[sign] + ' Available.')

        local_system_time = datetime.datetime.utcnow()
        local_system_utc = pytz.utc.localize(local_system_time)

        fe.pubdate(local_system_utc)


def oldToFeed(Signs):
    for sign in Signs:
        fe = fg.add_entry()
        fe.title(sign[0])
        fe.pubdate(sign[1])


def updateFeed():
    feed = BeautifulSoup(open('rss.xml'), "lxml")
    #Get the information from the previous feed.
    fg.title(feed.find('title').getText())
    fg.link(href=feed.link.nextSibling)
    fg.subtitle(feed.find('description').getText())
    fg.language('en')
    rssfeed = fg.rss_str(pretty=True)

    oldSigns = []

    #Get the items in the feed
    items = feed.findChildren('item')
    for item in items:
        oldSigns.append((item.find('title').getText(), item.find('pubdate').getText()))

    #Add old items to the new feed.
    oldToFeed(oldSigns)



def main():

    if not os.path.isfile("rss.xml"):
        createRSS() #Only used if no previous RSS Feed
        exportFeed() #Generate feed files.

    Signs = getSigns() #Get New Signs from Website
    updateFeed() #Get current feed.
    newSigns = getNew(Signs) #Get the new signs.
    newToFeed(newSigns) #Add New Signs to Feed
    exportFeed() #Write Feed to local RSS & Atom files.
    exportToJSON(Signs) #Export current list of signs (New + Old) to JSON File.
    exportForTwitter(newSigns) #Export new signs for Twitter Bot.

    subprocess.call("./exportRSS.sh", shell=True) #Calls Bash Script to send RSS & Atom file to webserver.

if __name__ == "__main__":
    main()
