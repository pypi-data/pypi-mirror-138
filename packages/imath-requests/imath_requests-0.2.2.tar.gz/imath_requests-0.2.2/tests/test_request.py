"""
test_request.py
====================================
Unit testing for request module
"""

import unittest
from imath_requests.request import PartData, PartProperty
from imath_requests.request import Position, Dimension
from imath_requests.server import create_app
import requests
import multiprocessing


class TestPosition(unittest.TestCase):
    """
    Unit testing for Position class in requests module.

    """
    def test_init_position(self):
        position = Position(44.2, 17.4, 0.0)

    def test_position_json(self):
        position = Position(44.2, 17.4, 0.0)
        position_json = position.to_json()
        # TODO add position json generation test


class TestDimension(unittest.TestCase):
    """
    Unit testing for Dimension class in requests module.

    """
    def test_init_dimension(self):
        dimension = Dimension(44.2, 17.4, 0.0)

    def test_dimension_json(self):
        dimension = Dimension(5.2, 1.0, 0.0)
        dimension_json = dimension.to_json()
        # TODO add dimension json generation test


class TestRequestsPartData(unittest.TestCase):
    """
    Unit testing for PartData class in requests module.

    """
    def test_init_part_data(self):
        """
        Test generation of part data class
        """
        property_list = [
            PartProperty("Steel grade", "Grade01"),
            PartProperty("Heat number", "C1234566"),
            PartProperty("Rolling schedule", "Schedule1"),
            PartProperty("Analysis C", 0.2),
            PartProperty("Analysis Mn", 0.02),
            PartProperty("Rod length", 2500)
        ]
        part_data = PartData(
            "1516193959559", "Part1234", "I3DR_DESKTOP_ABC123", property_list)

    def test_part_data_json(self):
        """
        Tests part data json generation.

        """
        property_list = [
            PartProperty("Steel grade", "Grade01"),
            PartProperty("Heat number", "C1234566"),
            PartProperty("Rolling schedule", "Schedule1"),
            PartProperty("Analysis C", 0.2),
            PartProperty("Analysis Mn", 0.02),
            PartProperty("Rod length", 2500)
        ]
        part_data = PartData(
            "1516193959559", "Part1234", "I3DR_DESKTOP_ABC123", property_list)
        part_data.to_json()
        # TODO add part data json generation test


class TestPartDataEndpoint(unittest.TestCase):
    """
    Unit testing part data in requests with mock server.

    """
    def setUp(self):
        self.server_name = "127.0.0.1:5000"
        self.server_username = "test"
        self.server_password = "test"
        self.app, self.api = create_app({'SERVER_NAME': self.server_name})
        self.app_thread = multiprocessing.Process(target=self.app.run)
        self.app_thread.start()
        # poll server to check it's ready for testing
        while True:
            try:
                requests.get(
                    "http://{}/".format(self.server_name), timeout=0.5)
                return
            except requests.exceptions.ConnectionError:
                pass

    def tearDown(self):
        self.app_thread.terminate()

    def test_part_data_get(self):
        part_data = PartData.get(
            self.server_name,
            self.server_username,
            self.server_password)
        self.assertIsNotNone(part_data)

    def test_part_data_post(self):
        property_list = [
            PartProperty("Steel grade", "Grade01"),
            PartProperty("Heat number", "C1234566"),
            PartProperty("Rolling schedule", "Schedule1"),
            PartProperty("Analysis C", 0.2),
            PartProperty("Analysis Mn", 0.02),
            PartProperty("Rod length", 2500)
        ]
        part_data = PartData(
            "1516193959559", "Part1234", "I3DR_DESKTOP_ABC123", property_list)
        resp = part_data.post(
            self.server_name,
            self.server_username,
            self.server_password)
        self.assertEqual(resp.status_code, 201)


if __name__ == '__main__':
    unittest.main()
