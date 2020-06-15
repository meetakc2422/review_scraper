from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS,cross_origin
from urllib.request import urlopen as uReq
import requests
from bs4 import BeautifulSoup as bs


reviews_app = Flask(__name__)
@reviews_app.route("/", methods= ['GET'])
@cross_origin()
def home():
  return render_template('index.html')

@reviews_app.route("/review", methods=['GET','POST'])
@cross_origin()
def index():
    if request.method == 'POST':

        try:
            searchkey = request.form['content'].replace(" ","")
            flipkart_url =  "https://www.flipkart.com/search?q=" + searchkey
            uClient = uReq(flipkart_url)
            b = uClient.read()
            uClient.close()
            tree = bs(b, "html.parser")
            a = tree.findAll("div", {"class": "bhgxx2 col-12-12"})
            del a[0:3]
            c = a[0]
            d = c.div.div.div.a["href"]
            prodlink = "https://www.flipkart.com" + d
            req = requests.get(prodlink)
            req.encoding='utf-8'
            reqhtml = bs(req.text, "html.parser")
            print(reqhtml)
            cmmnt = reqhtml.findAll('div', {'class': "_3nrCtb"})


            filename = searchkey + ".csv"
            fw = open(filename, "w")
            headers = "product, Customer name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []

            for info in cmmnt:
                    try:
                        name = info.div.div.find_all('p', {"class": "_3LYOAd _3sxSiS"})[0].text
                    except:
                        name = "Anonymous"
                    try:
                        rating = info.div.div.div.div.text

                    except:
                        rating = 'No Rating'

                    try:
                        commentHead = info.div.div.div.p.text
                    except:
                        commentHead = 'No Comment Heading'
                    try:
                        comtag = info.div.div.find_all('div', {'class': ''})
                        custComment = comtag[0].div.text
                    except:
                        custComment = 'No Customer Comment'
                    mydict = {"Product": searchkey, "Name": name, "Rating": rating, "CommentHead": commentHead,
                              "Comment": custComment}
                    reviews.append(mydict)
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print("problem occurred: ", e)
            return 'something is wrong'

                                                
    else:
      return render_template('index.html')

if __name__ == "__main__":
    # reviews_app.run(port=8000,debug=True)
    reviews_app.run(debug=True)





