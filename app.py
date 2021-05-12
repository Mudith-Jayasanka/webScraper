from flask import request , jsonify
from scraper import scrapper
import flask , flask_cors


myScraper = scrapper()

app = flask.Flask(__name__)
flask_cors.CORS(app)

@app.route("/reset",methods=["GET"])
def resetScraper():
    myScraper.reset()
    return "[SCRAPER]-Reset"

@app.route("/getNext" , methods=["GET"])
def getNext():
    myScraper.nextSoup()
    quote = {
        "quote" : myScraper.getQuote(),
        "author" : myScraper.getAuthorName(),
        "bio" : myScraper.getAuthorBio()
    }
    return quote

@app.route("/getAmount" , methods=["GET" , "POST"])
def getNextAmount():
    data = request.get_data().decode('utf-8')
    quote_arr = []
    for x in range(int(data)):
        quote_arr.append(getNext())
    return jsonify(quote_arr)

if __name__ == '__main__':
    app.run(debug=True)

