from flask import Flask, render_template
import utils
import scraper


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
	mapping = scraper.getMap()
	listingObjs = scraper.getListingObjs(mapping)
	output = render_template("index.html", listings = listingObjs)
	return output

if __name__ == "__main__":
	app.debug = True
	app.run()