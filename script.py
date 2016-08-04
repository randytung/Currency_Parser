import requests
from lxml import html
import lxml
import json

#sends a get request and returns a response
r = requests.get('https://www.federalreserve.gov/releases/h10/hist/default.htm')

#uses the response object to access the HTML from the currency website
tree = html.fromstring(r.content)

#Gets all of the countries and their URLs with the xpath. Since the rows are always in a /table//tr,
#and the country information will always be in the /a, this path will access the list of all 
#of the country HTML elements, regardless of the column. 
countries = tree.xpath('//*[@id="printThis"]/table//tr//a/@href')

#create a base URL to make it easier to access the currency exchange rates
base_url = 'https://www.federalreserve.gov/releases/h10/hist/'

#dictionary that will later be cast to a json
data = {}

#iterate through all of the countries
for country_url in countries:
  #if statement to only allow valid conversion URLs to be processed
  if country_url[-4:] == ".htm":
    #create the url for the country
    currency_request = requests.get(base_url + country_url)
    currency_tree = html.fromstring(currency_request.content)

    #this path will access the text of the header, which is the title of the currency
    title = currency_tree.xpath('//*[@id="printThis"]/h3/text()')[0].strip()

    #dictionary to represent the dates and currency rates of a country
    data[title] = {}

    #iterate through all of the currency rates in the country
    tree = currency_tree.xpath('//*[@id="printThis"]/table/tr')
    for row in tree:

      date = row[0].text
      us_rate = row[1].text.strip()
      data[title][date] = us_rate

    #print the title of the currency to verify that the forloop is iterating
    print title

#command to open the data file and write the json inside it
with open('data.json', 'w') as outfile:
  json.dump(data, outfile)




#FXcompared Web scraping Challenge

#1. Ensure your scraper would still work if column locations were to be changed. 
#   For example, if 'Country' column moved to the last column your code would
#   not break.
# 
# ---------- Path = //*[@id="printThis"]/table//tr//a/@href -----------------
# Since the rows are always in /table//tr, and the country information will 
#   always be in /a, this path will access the list of all of the country 
#   HTML elements, regardless of the column that the countries are located in.

#2. Optimize for efficiency in your coding in terms of making as few requests 
#   to host server as you can. 
#
#   In total, this script will make as many requests as the number of currencies
#   that are available in the currency website, plus one request to access 
#   the original page. I think that this is the minimum number of requests this script
#   can make because in order to access all of the information on the HTML page, 
#   it must access the original page as well as all of the other currency pages. 

#3. Use only these third-party libraries in addition to modules provided by Python: requests, lxml
#
# I used the request library in order to receive the response from the webpage,
# and the access and parse the HTML.

#4. Capture output results in JSON format written to disk.
#
# The last two lines of the script will output the file as a json. Even if the 
# file does not exist, or if it is empty, it will create the 'data.json' file.