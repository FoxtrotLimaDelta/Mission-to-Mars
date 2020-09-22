from flask import Flask, render_template, redirect
from  flask_pymongo import PyMongo
import scrapy

 # Flask Setup Flask Routes
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
# create route that renders index.html template
@app.route("/")
def Home():
    mars=mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scraper():
   mars = mongo.db.mars
   mars_data = scrapy.scraper()
   mars.update({}, mars_data, upsert=True)
   return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)