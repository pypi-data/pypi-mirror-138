from flask import Blueprint


boe = Blueprint(
    "boe", __name__)


def page():
    return "Hello, boe!"


boe.add_url_rule(
    "/boe/page", view_func=page)


def get_blueprints():
    return [boe]
