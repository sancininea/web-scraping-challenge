from flask import Flask, render_template, Markup
import pymongo
from scrape_mars import scrape

# Crear conexión con mongo
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Conectarse a la bd
db = client.marsBD

app=Flask(__name__)

@app.route("/")
def index():
    facts = list(db.marsStuff.find())[0]
    table_data = Markup(facts['html_table'])
    return render_template("index.html", stuff=facts, otherstuff=table_data)

@app.route("/scrape")
def scraping():
    results = scrape()
    db.marsStuff.insert_many([results])
    return "Done! Please go back to the main page, please, please, pleaaassseeee"

if __name__=="__main__":
    app.run(debug=True)