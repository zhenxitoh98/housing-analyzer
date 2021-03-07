from flask import request, jsonify, render_template, Blueprint
from database import property_ref, search_database
import json

search_query = Blueprint('search', __name__)


@search_query.route("/search")
def search():
    data = request.args
    city = data["city"].capitalize()
    zipcode = data["zipcode"].capitalize()
    state = data["state"].capitalize()
    minPrice = int(data["minPrice"])
    maxPrice = int(data["maxPrice"])

    results = []
    if city and zipcode and state:
        results = property_ref.where('address.city', '==', city).where('address.state', '==', state) \
            .where('address.postal_code', '==', zipcode).where('price', '>=', minPrice) \
            .where('price', '<=', maxPrice).get()
    elif city and state and zipcode == "":
        results = property_ref.where('address.city', '==', city).where('address.state', '==', state)\
            .where('price', '>=', minPrice).where('price', '<=', maxPrice).get()
    elif city and zipcode and state == "":
        results = property_ref.where('address.city', '==', city).where('address.postal_code', '==', zipcode)\
            .where('price', '>=', minPrice) \
            .where('price', '<=', maxPrice).get()
    elif state and zipcode and city == "":
        results = property_ref.where('address.state', '==', state).where('address.postal_code', '==', zipcode)\
            .where('price', '>=', minPrice) \
            .where('price', '<=', maxPrice).get()
    elif city and state == "" and zipcode == "":
        results = property_ref.where('address.city', '==', city).where('price', '>=', minPrice)\
            .where('price', '<=', maxPrice).get()
    elif state and city == "" and zipcode == "":
        results = property_ref.where('address.state', '==', state).where('price', '>=', minPrice) \
            .where('price', '<=', maxPrice).get()
    elif zipcode and state == "" and city == "":
        results = property_ref.where('address.postal_code', '==', zipcode).where('price', '>=', minPrice) \
            .where('price', '<=', maxPrice).get()
    else:
        results = property_ref.where('price', '>=', minPrice).where('price', '<=', maxPrice).get()

    new_results = []
    if len(results) > 0:
        for result in results:
            new_results.append(result.to_dict())
    else:
        results = search_database(city, "GA")
        state = "Georgia"
        for result in results:
            new_results.append(result)

    return render_template("search_results.html", results=new_results, city=city, state=state)