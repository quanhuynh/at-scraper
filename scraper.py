import requests
import bs4
import re
import utils

#getMap
#this function maps the title to the link of the individual postings on a forum page
#return list of titles of listings, mapped to the link of the listing
def getMap(pageNum=1):
	titleLinkMapping = {}
	link = "http://www.archerytalk.com/vb/forumdisplay.php?f=99" + "&page=" + str(pageNum)
	response = requests.get(link)
	soup = bs4.BeautifulSoup(response.text)
	#titles = [''.join(t.findAll(text=True)) for t in soup.findAll('a', {'class':'title'})]
	aTags = soup.findAll('a', {'class': 'title'})
	for a in aTags:
		title = a.text
		url = a['href']
		titleLinkMapping[title] = url

	return titleLinkMapping


#createListing
#this function parses the text in the actual post
#return a Listing object from the title and link
def createListing(title, link):
	postResponse = requests.get("http://www.archerytalk.com/vb/" + link)
	soup = bs4.BeautifulSoup(postResponse.text)
	firstPost = soup.find('li', {'class':'postbit'})

	#POSTING TIME
	timeStamp = firstPost.find('span', {'class':'date'})
	date = timeStamp.find('span').previousSibling.replace(',\xa0', '')

	#CONTENT
	textContent = firstPost.find('blockquote', {'class':'postcontent'})
	listingObj = parse(textContent.text, title, link)
	return listingObj


#parse
#this function creates Listing object from strings text, title and link
#returns a Listing object
def parse(text, title, link):
	brand = "unknown"
	weight = "unknown"
	length = []
	price = "unknown"
	color = "unknown"

	titleWords = title.split(" ")

	#Check words and classify
	contentWords = text.strip().replace("\r\n", " ").split(" ") + titleWords
	#print(contentWords)
	for i in range(len(contentWords)):
		word = contentWords[i].lower()
		##Brand check
		if brand == "unknown" and word in utils.BRANDS:
			brand = word
			continue
		##Color check
		if color == "unknown" and word in utils.COLORS:
			color = word
			continue
		##Price filter/check
		priceFilter = word.replace("$", "").replace("tyd", "").replace("obo", "")
		if price == "unknown" and priceFilter in utils.PRICES:
			price = priceFilter
			continue
		##Length filter/check
		lengthFilter = word.replace('"', "").replace("in", "").replace("inch", "")
		if lengthFilter in utils.DRAWLENGTHS:
			length.append(lengthFilter)
			continue
		##Weight filter/check
		weightFilter = word.replace("lb", "").replace("lbs", "").replace("#", "")
		if weight == "unknown" and weightFilter in utils.DRAWWEIGHTS:
			weight = weightFilter
			continue

	return Listing(title, link, brand, weight, length, price, color)

#getListingObjs
#this function gets all the Listing objects given a mapping of titles and links
#returns a list of Listings
def getListingObjs(mapping):
	listings = [createListing(t, mapping[t]) for t in mapping.keys()]
	return listings


#class describing a single Listing
class Listing():
	def __init__(self, title, link, brand="other", weight="unknown", length="unknown", price="unknown", color="unknown"):
		self._title = title
		self._link = link
		self._brand = brand
		self._weight = weight
		self._length = length
		self._price = price
		self._color = color
		
	def title(self):
		return self._title

	def brand(self):
		return self._brand

	def price(self):
		return self._price

	def __str__(self):
		
		return "Title: " + self._title + "\n" \
		"Brand: " + self._brand + "\n" + \
		"Color: " + self._color + "\n" + \
		"Weight: " + self._weight + "\n" + \
		"Length: " + str(self._length) + "\n" + \
		"Price: " + self._price + "\n" \