#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app
import unittest
import flask
from flask import request, jsonify
import json

class FlaskTest(unittest.TestCase):
    
    #resposta 200 
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        status_code  = response.status_code 

        self.assertEqual(status_code, 200)

    #Testa user incorreto
    def test_user_incorreto(self):
        tester = app.test_client(self)
        response = tester.get("/basket/events?user=AAA")
        self.assertTrue(b'user nao existe' in response.data)

if __name__ == "__main__":
    unittest.main() 
