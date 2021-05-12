from scraper import scrapper
import flask , flask_cors
import jsonify

myScraper = scrapper()

app = flask.Flask(__name__)
flask_cors.CORS(app)

@app.route("/reset",methods=["GET"])
def resetScraper():
    myScraper.reset()
    return jsonify("[SCRAPER]-Reset")

@app.route("/getNext" , methods=["GET"])
def getNext():
    quote = {
        "quote" : myScraper.getQuote(),
        "author" : myScraper.getAuthorName(),
        "bio" : myScraper.getAuthorBio()
    }
    myScraper.nextSoup()
    return quote

if __name__ == '__main__':
    app.run(debug=True)

