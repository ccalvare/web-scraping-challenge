#MongoDB and Flask 
#######################

#Import Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

####################################
#PyMongo Connection
####################################
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

####################################
#Flask Route
####################################
#Routes
@app.route("/")
def index():
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars_data)


# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
@app.route("/scrape")
def scrape():
    #Run the Scrape
    mars_data_info = scrape_mars.scrape_info()

    #Update to Mongo
    mongo.db.collection.update({}, mars_data_info, upsert=True)

    return redirect("/")


# Define Main Behavior
if __name__ == "__main__":
    app.run(debug=True)