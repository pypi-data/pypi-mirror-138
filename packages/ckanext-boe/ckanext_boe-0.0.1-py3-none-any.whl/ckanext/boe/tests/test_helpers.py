"""Tests for helpers.py."""

import ckanext.boe.helpers as helpers


def test_boe_hello():
    assert helpers.boe_hello() == "Hello, boe!"
