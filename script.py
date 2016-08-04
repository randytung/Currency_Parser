import requests
from lxml import html
import lxml
import json

#sends a get request and returns a response
r = requests.get('https://www.federalreserve.gov/releases/h10/hist/default.htm')
