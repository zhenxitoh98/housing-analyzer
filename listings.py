from flask import Blueprint, render_template, request
from database import property_ref

listings = Blueprint('listings', __name__)


@listings.route("/listing/<property_id>")
def listing(property_id):
    result = property_ref.document(property_id).get().to_dict()
    return render_template("listing.html", result=result)



