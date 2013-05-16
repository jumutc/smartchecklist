"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.utils import unittest
from SmartChecklist.calculations import *

def test_contains(self, items, length):
    self.assertEquals('sugar', items[length-3])
    self.assertEquals('napkins', items[length-2])
    self.assertEquals('bread', items[length-1])
    self.assertEqual(length, len(items))

def test_contains1(self, items):
    self.assertEquals('milk', items[0])
    test_contains(self, items, 4)

def test_contains2(self, items):
    self.assertEquals('0,25 milk', items[0])
    test_contains(self, items, 4)

def test_contains3(self, items):
    self.assertEquals('test', items[0])
    self.assertEquals('0,25 milk', items[1])
    test_contains(self, items, 5)

def test_contains4(self, items):
    self.assertEquals('test', items[0])
    self.assertEquals('0,25', items[1])
    test_contains(self, items, 5)


class CalculationsTest(unittest.TestCase):

    def test_get_delimited_items(self):
        items = get_delimited_items('Buy me some milk sugar napkins and bread')
        test_contains1(self, items)

        items = get_delimited_items('milk, sugar, napkins and bread')
        test_contains1(self, items)

        items = get_delimited_items('milk;sugar;napkins;bread')
        test_contains1(self, items)

        items = get_delimited_items(',milk;sugar;napkins;bread?')
        test_contains1(self, items)

        items = get_delimited_items('0,25 milk, sugar, napkins and bread')
        test_contains2(self, items)

        items = get_delimited_items(';0,25 milk, sugar, napkins and bread;')
        test_contains2(self, items)

        items = get_delimited_items('test;0,25 milk, sugar, napkins and bread;')
        test_contains3(self, items)

        items = get_delimited_items('test;0,25; sugar, napkins and bread;')
        test_contains4(self, items)



