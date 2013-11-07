#
# Scrapes games.
#

import bs4
import csv
import codecs
import urllib2

import appUrls
import gameUrls

# whether to only scrape productivity apps.
productivityAppsOnly = True

# a list of urls of app pages to scrape.
# urls = gameUrls.gameUrls
urls = appUrls.appUrls

# open a csv file for writing into.
dataFile = open('productivityApps.csv', mode='w')
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

    # get the category of the app.
    categoryNode = soup.find('span', itemprop='genre')
    category = processUnicode(getCategory(categoryNode.get_text().strip()))
    if productivityAppsOnly and category != "Productivity":
        # only scrape productivity apps.
        print 'Ignoring ' + category + ' app ' + appName
        continue

    # append the app name.
    row.append(appName)

    # includes the category of the game.
    row.append(category)

    # get the icon URL.
    iconNode = soup.find('img', class_='cover-image')
    iconUrl = iconNode['src']
    row.append(iconUrl)

    # get discretized number of installs.
    numInstallsNode = soup.find('div', itemprop='numDownloads')
    numDownloads = processUnicode(numInstallsNode.get_text().strip())
    row.append(numDownloads)

    # get the app release date.
    appUpdatedDateNode = soup.find('div', class_='document-subtitle')
    updateDate = processUnicode(appUpdatedDateNode.get_text()[1:].strip())
    row.append(updateDate)

    # get the app's description.
    descriptionNode = soup.find('div', class_='app-orig-desc')
    description = processUnicode(descriptionNode.get_text())
    row.append(description)

    # write our row into the csv file.
    writer.writerow(row)

    # update status.
    numAppsProcessed += 1
    print 'Processed ' + str(numAppsProcessed) + ' apps. Last one: ' + \
        appName

