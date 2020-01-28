#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 18:20:27 2020

@author: shane
"""

import os
import subprocess
import threading

import gunicorn
from flask import Flask, request
from flask_cors import CORS

from ntserv.accounts import GET_favorites, GET_logs, GET_rdas, POST_login, POST_register
from ntserv.libserver import Request, Response, home_page_text, self_route_rules
from ntserv.shop import (
    GET_products__product_id__reviews,
    GET_products_avg_ratings,
    GET_stripe_products,
    GET_stripe_skus,
    POST_products_reviews,
)
from ntserv.usda import (
    GET_analyze,
    GET_biometrics,
    GET_exercises,
    GET_fdgrp,
    GET_nutrients,
    GET_search,
    GET_serving_sizes,
)
from ntserv.utils.caffeine import caffeinate

# Export the Flask server for gunicorn
app = Flask(__name__)
CORS(app)
caffeinate()


"""
-------------------------
Routes
-------------------------
"""


@app.route("/")
def get_home_page():
    url_map = self_route_rules(app)
    home_page = home_page_text(url_map)
    return f"<pre>{home_page}</pre>"


"""
-------------------------
Account functions
-------------------------
"""


@app.route("/register", methods=["POST"])
def post_register():
    return Request(POST_register, request)


@app.route("/login", methods=["POST"])
def post_login():
    return Request(POST_login, request)


"""
-------------------------
Basic DB functions
-------------------------
"""


@app.route("/fdgrp")
def get_fdgrp():
    return Request(GET_fdgrp, request)


@app.route("/serving_sizes")
def get_serving_sizes():
    return Request(GET_serving_sizes, request)


@app.route("/nutrients")
def get_nutrients():
    return Request(GET_nutrients, request)


@app.route("/exercises")
def get_exercises():
    return Request(GET_exercises, request)


@app.route("/biometrics")
def get_biometrics():
    return Request(GET_biometrics, request)


@app.route("/search")
def get_search():
    return Request(GET_search, request)


@app.route("/analyze")
def get_analyze():
    return Request(GET_analyze, request)


"""
-------------------------
Private DB functions
-------------------------
"""


@app.route("/favorites")
def get_favorites():
    return Request(GET_favorites, request)


@app.route("/rdas")
def get_rdas():
    return Request(GET_rdas, request)


@app.route("/logs")
def get_logs():
    return Request(GET_logs, request)


"""
-------------------------
Stripe functions
-------------------------
"""


@app.route("/stripe/products")
def get_stripe_products():
    return Request(GET_stripe_products, request)


@app.route("/stripe/skus")
def get_stripe_skus():
    return Request(GET_stripe_skus, request)


@app.route("/products/<id>/reviews")
def get_products__product_id__reviews(id):
    return Request(GET_products__product_id__reviews, request)


@app.route("/products/reviews", methods=["POST"])
def post_products_reviews():
    return Request(POST_products_reviews, request)


@app.route("/products/avg_ratings")
def get_products_avg_ratings():
    return Request(GET_products_avg_ratings, request)


# Make script executable
if __name__ == "__main__":
    """ Run as file (or debug it in vscode!) """

    print("[__main__] bypassing gunicorn...")
    port = int(os.getenv("PORT", 20000))
    app.run(
        host="127.0.0.1", port=port, debug=True,
    )
