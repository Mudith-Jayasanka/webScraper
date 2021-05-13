import time
from bs4 import BeautifulSoup
from urllib.request import urlopen


class scrapper():

    def __init__(self):
        self.soup = ""
        self.soupIndex = 1200
        self.soup = self.nextSoup()
        

    def getQuote(self):
        def decomposeAll(html_data , tag):
            while(html_data.find(tag) is not None):
                html_data.find(tag).decompose()
            return html_data

        def assembleQuote(soloSegments , anchorSegments):
            #Assembles the seperated quote
            quote = ""
            while (len(soloSegments) > 0) or (len(anchored_segments) > 0):
                if len(soloSegments) > 0:
                    quote += soloSegments.pop(0)
                if len(anchored_segments) > 0:
                    quote += " " + anchorSegments.pop(0) + " "
            return quote

        def getAllAnchorText(anchorList):
            text =[]
            for anchor in anchorList:
                text.append(anchor.text)
            return text

        #The single quote is broken into <quote segment> , <a><quote segment></a> this pattern
        quote_html = self.soup.find("div" , id="page-container").find("div" , class_="row").find("div",id="content-body").find("h1",id="disp-quote-body")
        quote_anchors = quote_html.find_all("a")

        anchored_segments = getAllAnchorText(quote_anchors)

        quote_html = decomposeAll(quote_html , "a")
        non_anchored_segments = quote_html.text.split("  ")

        quote = assembleQuote(non_anchored_segments , anchored_segments)
        return quote

    def getAuthorName(self):
        return self.soup.find("div" , id="disp-quote-author-meta").find("p",class_="author").a.text

    def getAuthorBio(self):
        return self.soup.find("div" , id="disp-quote-author-meta").find("p" , class_="author-bio").text

    def nextSoup(self):
        print("Current SoupIndex : " + str(self.soupIndex))
        client = urlopen("https://www.quotes.net/quote/" + str(self.soupIndex))
        page_html = client.read()
        client.close()
        soup = BeautifulSoup(page_html , "lxml")
        self.soupIndex += 1
        self.soup = soup
        return soup

    def displayQuotes(self , count):
        startTime = time.time()
        print("------------------------------")
        for x in range(count):
            self.nextSoup()
            print(self.getQuote() )
            print()
            print("BIO - " + self.getAuthorBio() )
            print()
            print("Author - " + self.getAuthorName())
            print("------------------------------")
        total = time.time() - startTime
        print("Elapsed Time : Sec ->" + str(total))

    def reset(self):
        self.soupIndex = 2
    
    def setSoupIndex(self , index):
        self.soupIndex = index


