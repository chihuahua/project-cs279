#
# Scrapes games.
#

import MySQLdb
import bs4
import csv
import urllib2

import gameUrls

# a list of urls of app pages to scrape.
urls = gameUrls.gameUrls

# # open a csv file for writing into.
# dataFile = open('apps.csv', 'w')

# # create a writer for writing csv data.
# writer = csv.writer(dataFile, delimiter=',', quotechar='"',
#     quoting=csv.QUOTE_MINIMAL)

# connect to database, and create a cursor for navigating in the database.
db = MySQLdb.connect(host="sql.279.chizeng.com", user="cs279",
    passwd="harvard08", db="279project")
cursor = db.cursor()

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

def getCategory(categoryTitle):
  '''
  Gets the category of the app.
  '''
  if categoryTitle in gameCategories:
    return 'Game'
  return categoryTitle

if __name__ == '__main__':
  # open all urls.
  for url in urls:
    # store data in a row to be written later.
    row = []

    # get the html for that page.
    httpResponse = urllib2.urlopen(url)
    if not httpResponse:
      print url + ' not openable.'
      exit(1)

    html = httpResponse.read()

    # parse the html of the page.
    soup = bs4.BeautifulSoup(html)

    # get the app name.
    appNameNode = soup.find('div', class_='document-title')
    appName = appNameNode.get_text().strip()
    row.append(appName)

    # gets the category of the game.
    categoryNode = soup.find('span', itemprop='genre')
    category = getCategory(categoryNode.get_text().strip())
    row.append(category)

    # get the icon URL.
    iconNode = soup.find('img', class_='cover-image')
    iconUrl = iconNode['src']
    row.append(iconUrl)

    # get discretized number of installs.
    numInstallsNode = soup.find('div', itemprop='numDownloads')
    numDownloads = numInstallsNode.get_text().strip()
    row.append(numDownloads)

    # get the app release date.
    appUpdatedDateNode = soup.find('div', class_='document-subtitle')
    updateDate = appUpdatedDateNode.get_text()[1:].strip()
    row.append(updateDate)

    # get the app's description.
    descriptionNode = soup.find('div', class_='app-orig-desc')
    description = descriptionNode.get_text()
    row.append(description)
