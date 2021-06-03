from flask import Flask, render_template, request
from listings import listings
from search_query import search_query
from database import property_ref
from collections import defaultdict, Counter
from statistics import mean
from operator import itemgetter
import json


app = Flask(__name__)
app.register_blueprint(listings)
app.register_blueprint(search_query)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/map/<state>")
def map1(state):
    state = state or 'Georgia'
    cached_file = "data" + "-" + state + ".json"
    html_file = "map" + "-" + state.lower() + ".html"

    try:
        #Simulating failed database call with Runtime errors. This limits load on database. To call directly, remove line
        #below.
        raise RuntimeError('Database call failed')

        results = property_ref.where('address.state', '==', state).get()

        new_results = []
        if len(results) > 0:
            for result in results:
                new_results.append(result.to_dict())
    except RuntimeError:
        #if database call fails pull from locally stored json
        with open(cached_file, 'r') as j:
            new_results = json.loads(j.read())

    if len(new_results) > 0:
        with open(cached_file, 'w', encoding='utf-8') as f:
            json.dump(new_results, f, ensure_ascii=False, indent=4)

    data = defaultdict(list)
    number_of_houses_without_building_size = 0

    for i in range(0, len(new_results)):
        price = new_results[i]['price']
        if not new_results[i]['address'].get('county') or not new_results[i]['address'].get('postal_code'):
            continue
        county = new_results[i]['address']['county']
        zipcode = new_results[i]['address']['postal_code']
        if price == 0:
            continue
        if new_results[i].get('price') and new_results[i].get('building_size') and new_results[i]['building_size'].get('size'):
            price_per_square_feet = new_results[i]['price'] / new_results[i]['building_size']['size']
        else:
            number_of_houses_without_building_size += 1
            continue

        data[county].append((price, price_per_square_feet, zipcode))

    counties = {}
    min_prices = []
    max_prices = []
    average_prices = []
    average_prices_per_square_feet = []
    zipcodes = []

    for i, county in enumerate(data):
        list_of_prices = data[county]

        max_price = float('-inf')
        min_price = float('inf')
        average_price = 0
        average_price_per_sq_ft = 0
        for price_and_price_per_square_foot in list_of_prices:
            min_price = min(min_price, price_and_price_per_square_foot[0])
            max_price = max(max_price, price_and_price_per_square_foot[0])
            average_price += price_and_price_per_square_foot[0]
            average_price_per_sq_ft += price_and_price_per_square_foot[1]
        counties[county] = i

        min_prices.append(min_price)
        max_prices.append(max_price)
        zipcodes.append(price_and_price_per_square_foot[2])
        average_prices.append(average_price / len(list_of_prices))
        average_prices_per_square_feet.append(average_price_per_sq_ft / len(list_of_prices))

    return render_template(
        html_file,
        counties=counties,
        min_prices=min_prices,
        max_prices=max_prices,
        average_prices=average_prices,
        average_prices_per_square_feet=average_prices_per_square_feet,
        max_price=max(average_prices),
        min_price=min(average_prices),
        zipcodes=zipcodes
    )


@app.route("/average-chart/<state>")
def average(state):
    results = property_ref.where('address.state', '==', state).get()

    new_results = []
    if len(results) > 0:
        for result in results:
            new_results.append(result.to_dict())

    data = defaultdict(list)

    for i in range(0, len(new_results)):
        if new_results[i]['price'] is not None:
            data[new_results[i]['address']['postal_code']].append(new_results[i]['price'])

    avg_data = dict()

    for d in data:
        avg_data[d] = round(mean(data[d]), 2)

    zipcode = list(avg_data.keys())
    price = list(avg_data.values())

    return render_template("average-chart.html", zipcode=zipcode, price=price, state=state)

@app.route("/top-max-chart/<state>")
def top_max_chart(state):
    results = property_ref.where('address.state', '==', state).get()

    new_results = []
    if len(results) > 0:
        for result in results:
            new_results.append(result.to_dict())

    data = defaultdict(list)

    for i in range(0, len(new_results)):
        if new_results[i]['price'] is not None:
            data[new_results[i]['address']['postal_code']].append(new_results[i]['price'])

    avg_data = dict()

    for d in data:
        avg_data[d] = round(mean(data[d]), 2)

    k = Counter(avg_data)
    top_6 = k.most_common(6)

    zipcode = list(i[0] for i in top_6)
    price = list(i[1] for i in top_6)

    return render_template("top_max_chart.html", zipcode=zipcode, price=price, state=state)

@app.route("/top-min-chart/<state>")
def top_min_chart(state):
    results = property_ref.where('address.state', '==', state).get()

    new_results = []
    if len(results) > 0:
        for result in results:
            new_results.append(result.to_dict())

    data = defaultdict(list)

    for i in range(0, len(new_results)):
        if new_results[i]['price'] is not None:
            data[new_results[i]['address']['postal_code']].append(new_results[i]['price'])

    avg_data = dict()

    for d in data:
        avg_data[d] = round(mean(data[d]), 2)

    res = dict(sorted(avg_data.items(), key=itemgetter(1))[:6])
    zipcode = list(res.keys())
    price = list(res.values())

    return render_template("top_min_chart.html", zipcode=zipcode, price=price, state=state)

@app.route("/min-max-chart/<state>")
def min_max_chart(state):
    results = property_ref.where('address.state', '==', state).get()

    new_results = []
    if len(results) > 0:
        for result in results:
            new_results.append(result.to_dict())

    data = defaultdict(list)

    for i in range(0, len(new_results)):
        data[new_results[i]['address']['postal_code']].append(new_results[i]['price'])

    average_data = dict()
    min_data = dict()
    max_data = dict()

    for d in data:
        if data[d]:
            average_data[d] = round(mean(x for x in data[d] if x is not None), 2)
            min_data[d] = min(x for x in data[d] if x is not None)
            max_data[d] = max(x for x in data[d] if x is not None)

    zipcode = list(average_data.keys())
    price = list(average_data.values())
    min_prices = list(min_data.values())
    max_prices = list(max_data.values())

    return render_template("min-max-chart.html", state=state, zipcode=zipcode, price=price,
                           min_prices=min_prices, max_prices=max_prices)


@app.route("/property-type-chart/<state>")
def property_type(state):
    single = property_ref.where('prop_type', '==', "single_family").where('address.state', '==', state).get()
    multi = property_ref.where('prop_type', '==', "multi_family").where('address.state', '==', state).get()
    condo = property_ref.where('prop_type', '==', "condo").where('address.state', '==', state).get()
    land = property_ref.where('prop_type', '==', "land").where('address.state', '==', state).get()

    single_results = []
    multi_results = []
    condo_results = []
    land_results = []

    if len(single) > 0:
        for result in single:
            single_results.append(result.to_dict())

    if len(multi) > 0:
        for result in multi:
            multi_results.append(result.to_dict())

    if len(condo) > 0:
        for result in condo:
            condo_results.append(result.to_dict())

    if len(land) > 0:
        for result in land:
            land_results.append(result.to_dict())

    single_data = dict()
    multi_data = dict()
    condo_data = dict()
    land_data = dict()

    for i in range(0, len(single_results)):
        if single_results[i]['address']['postal_code'] is not None:
            single_data[single_results[i]['address']['postal_code']] = single_data.get(single_results[i]
                                                                                       ['address']['postal_code'], 0) + 1

    for i in range(0, len(multi_results)):
        if multi_results[i]['address']['postal_code'] is not None:
            multi_data[multi_results[i]['address']['postal_code']] = multi_data.get(multi_results[i]
                                                                                    ['address']['postal_code'], 0) + 1

    for i in range(0, len(condo_results)):
        if condo_results[i]['address']['postal_code'] is not None:
            condo_data[condo_results[i]['address']['postal_code']] = condo_data.get(condo_results[i]
                                                                                    ['address']['postal_code'], 0) + 1

    for i in range(0, len(land_results)):
        if land_results[i]['address']['postal_code'] is not None:
            land_data[land_results[i]['address']['postal_code']] = land_data.get(land_results[i]
                                                                                    ['address']['postal_code'], 0) + 1

    for key in single_data.keys():
        if key not in multi_data.keys():
            multi_data[key] = 0

        if key not in condo_data.keys():
            condo_data[key] = 0

        if key not in land_data.keys():
            land_data[key] = 0

    for key in multi_data.keys():
        if key not in single_data.keys():
            single_data[key] = 0

        if key not in condo_data.keys():
            condo_data[key] = 0

        if key not in land_data.keys():
            land_data[key] = 0

    for key in condo_data.keys():
        if key not in single_data.keys():
            single_data[key] = 0

        if key not in multi_data.keys():
            multi_data[key] = 0

        if key not in land_data.keys():
            land_data[key] = 0

    for key in land_data.keys():
        if key not in single_data.keys():
            single_data[key] = 0

        if key not in multi_data.keys():
            multi_data[key] = 0

        if key not in condo_data.keys():
            condo_data[key] = 0

    sorted_single_data = dict(sorted(single_data.items()))
    sorted_multi_data = dict(sorted(multi_data.items()))
    sorted_condo_data = dict(sorted(condo_data.items()))
    sorted_land_data = dict(sorted(land_data.items()))

    zipcode = list(sorted_multi_data.keys())
    single_value = list(sorted_single_data.values())
    multi_value = list(sorted_multi_data.values())
    condo_value = list(sorted_condo_data.values())
    land_value = list(sorted_land_data.values())

    return render_template("property_type.html", zipcode=zipcode, state=state, single=single_value,
                           multi=multi_value, condo=condo_value, land=land_value)


if __name__ == '__main__':
    app.run('0.0.0.0', 8085, debug=True)