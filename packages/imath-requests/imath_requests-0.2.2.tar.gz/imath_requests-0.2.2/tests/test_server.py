"""
test_server.py
====================================
Unit testing for server module
"""

import unittest
import pytest
import tempfile
from imath_requests.server import create_app


class TestPartDataEndpoint(unittest.TestCase):
    """
    Unit testing for part data endpoint of app in Server module.

    """
    def setUp(self):
        app, api = create_app({'TESTING': True})
        self.client = app.test_client()

    def test_part_data_get(self):
        self.client.get('/imath-rest-backend/part', follow_redirects=True)

    def test_part_data_post(self):
        part_data = {
            "identifiedTime": 1516193959559,
            "partId": "Part1234",
            "source": "Camera_Control_PC_Garret",
            "partData": [
                {
                    "key": "steel_grade",
                    "value": "Grade01"
                },
                {
                    "key": "heat_number",
                    "value": "C1234566"
                },
                {
                    "key": "rolling_schedule",
                    "value": "Schedule1"
                }
            ]
        }
        self.client.post('/imath-rest-backend/part', data=part_data, follow_redirects=True)
