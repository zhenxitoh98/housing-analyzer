from flask import Flask, render_template
from listings import listings
from search_query import search_query


app = Flask(__name__)
app.register_blueprint(listings)
app.register_blueprint(search_query)


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == '__main__':
    app.run('0.0.0.0', 8085, debug=True)
