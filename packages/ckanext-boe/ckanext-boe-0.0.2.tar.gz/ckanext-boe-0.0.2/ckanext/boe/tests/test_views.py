"""Tests for views.py."""

import pytest

import ckanext.boe.validators as validators


import ckan.plugins.toolkit as tk


@pytest.mark.ckan_config("ckan.plugins", "boe")
@pytest.mark.usefixtures("with_plugins")
def test_boe_blueprint(app, reset_db):
    resp = app.get(tk.h.url_for("boe.page"))
    assert resp.status_code == 200
    assert resp.body == "Hello, boe!"
