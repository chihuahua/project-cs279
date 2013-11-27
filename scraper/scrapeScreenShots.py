# -*- coding: utf-8 -*-
#
# Scrapes games' screenshots. Saves into a CSV file in the format
# "Name", "App Page URL", "Screenshot URL"
#

import bs4
import csv
import codecs
import datetime
import sys
import urllib2

import appUrls
import gameUrls

# whether to only scrape productivity apps.
productivityAppsOnly = False

# a list of urls of app pages to scrape.
urls = gameUrls.gameUrls
# urls = appUrls.appUrls

# open a csv file for writing into.
dataFile = open('screenshotsGameApps.csv', mode='w')
dataFile.write(codecs.BOM_UTF8)

# create a writer for writing csv data.
writer = csv.writer(dataFile, delimiter=',', quotechar='"',
    quoting=csv.QUOTE_MINIMAL)

# connect to database, and create a cursor for navigating in the database.
# db = MySQLdb.connect(host="sql.279.chizeng.com", user="cs279",
#     passwd="harvard08", db="279project")
# cursor = db.cursor()

# categories of games.
gameCategories = frozenset([
    'Arcade & Action',
    'Brain & Puzzle',
    'Cards & Casino',
    'Casual',
    'Live Wallpaper',
    'Racing',
    'Sports Games',
    'Widgets'
  ])

def processUnicode(str):
    '''
    Processes unicode character in strings.
    '''
    return str.encode('utf-8')

def getCategory(categoryTitle):
  '''
  Gets the category of the app.
  '''
  if categoryTitle in gameCategories:
    return 'Game'
  return categoryTitle

if __name__ == '__main__':
  # write headers into the csv file.
  headers = ['name', 'category', 'icon', 'downloads', 'updateDate', \
     'description']
  writer.writerow(headers)

  # open all urls.
  numAppsProcessed = 0
  for url in urls:
    # store data in a row to be written later.
    row = []

    # get the html for that page.
    try:
        httpResponse = urllib2.urlopen(url)
    except urllib2.URLError, e:
        print 'Error opening ' + url
        continue

    html = httpResponse.read()

    # parse the html of the page.
    soup = bs4.BeautifulSoup(html)

    # get the name of the app.
    appNameNode = soup.find('div', class_='document-title')
    appName = processUnicode(appNameNode.get_text().strip())
    row.append(appName)

    # get the URL
    row.append(url)

    # get the first screenshot.
    screenShotUrlNode = soup.find('img', class_='screenshot')
    if not screenShotUrlNode:
      # keep going if no screenshot found.
      continue

    screenShotUrl = processUnicode(screenShotUrlNode['src'].strip())
    row.append(screenShotUrl)

    # write the data to a CSV file.
    writer.writerow(row)

    # update status.
    numAppsProcessed += 1
    print 'Processed ' + str(numAppsProcessed) + ' apps. Last one: ' + \
        appName
