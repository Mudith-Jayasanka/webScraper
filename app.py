from logging import error
from flask import request , jsonify
from scraper import scrapper
import flask , flask_cors
import hashlib


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
    continuousBigErrors = 0
    try:
        quote = {
        "quote" : myScraper.getQuote(),
        "author" : myScraper.getAuthorName(),
        "bio" : myScraper.getAuthorBio()
        }

        Author_bio_quote = quote["author"] + quote["bio"] + quote["quote"]
        try:
            hash_key = hashlib.sha256( Author_bio_quote.encode("utf8") )
            quote["hash-key"] = hash_key.hexdigest()
        except:
            print("--------------------------------")
            print("Tried to encode : " + Author_bio_quote)
            quote = getNext()
        continuousBigErrors = 0
    except:
        print("BIGGER ERROR")
        continuousBigErrors += 1
        if(continuousBigErrors  > 5): #Continuous errors in this case mean Quote mining has been completed
            return None
        quote = getNext()
    
    return quote

@app.route("/getAmount" , methods=["GET" , "POST"])
def getNextAmount():
    data = request.get_data().decode('utf-8')
    quote_arr = []
    for x in range(int(data)):
        nextQuote = getNext()
        if nextQuote is None:
            break
        quote_arr.append(nextQuote)
    return jsonify(quote_arr)

@app.route("/setStart" , methods=["GET" , "POST"])
def setIndex():
    data = request.get_data().decode('utf-8')
    myScraper.setSoupIndex(int(data))
    return jsonify("[index Set]-"+str(data))

if __name__ == '__main__':
    app.run(debug=True , use_reloader=False)

#Check this site to check the duplicate request issue
#https://stackoverflow.com/questions/14874782/apscheduler-in-flask-executes-twice