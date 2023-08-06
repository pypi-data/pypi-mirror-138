"""
test_request.py
====================================
Unit testing for request module
"""

import unittest
from imath_requests.request import PartData, ImageAnalysisData, ImageAnalysisFailure
from imath_requests.request import ImageValue, ImageMetaData
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
        position_json = position.get_json()
        # TODO add position json generation test


class TestDimension(unittest.TestCase):
    """
    Unit testing for Dimension class in requests module.

    """
    def test_init_dimension(self):
        dimension = Dimension(44.2, 17.4, 0.0)

    def test_dimension_json(self):
        dimension = Dimension(5.2, 1.0, 0.0)
        dimension_json = dimension.get_json()
        # TODO add dimension json generation test


class TestRequestsPartData(unittest.TestCase):
    """
    Unit testing for PartData class in requests module.

    """
    def test_init_part_data(self):
        """
        Test generation of part data class
        """
        part_data_list = [
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
            },
            {
                "key": "analysis",
                "value": [
                    {
                        "key": "C",
                        "value": "0.2"
                    },
                    {
                        "key": "Mn",
                        "value": "0.02"
                    }
                ]
            }
        ]
        part_data = PartData(
            "1516193959559", "Part1234", "I3DR_DESKTOP_ABC123", part_data_list)

    def test_part_data_json(self):
        """
        Tests part data json generation.

        """
        part_data_list = [
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
            },
            {
                "key": "analysis",
                "value": [
                    {
                        "key": "C",
                        "value": "0.2"
                    },
                    {
                        "key": "Mn",
                        "value": "0.02"
                    }
                ]
            }
        ]
        part_data = PartData(
            "1516193959559", "Part1234", "I3DR_DESKTOP_ABC123", part_data_list)
        part_data.get_json()
        # TODO add part data json generation test


class TestRequestsImageValue(unittest.TestCase):
    """
    Unit testing for ImageValue class in requests module.

    """
    def test_init_image_value(self):
        """
        Test generation of image value class
        """
        image_value = ImageValue(
            "test001.png", "1516193959559", Position(44.2, 17.4, 0.0),
            Dimension(5.2, 1.0, 0.0), "1"
        )

    def test_image_value_json(self):
        """
        Tests image value json generation.

        """
        image_value = ImageValue(
            "test001.png", "1516193959559", Position(44.2, 17.4, 0.0),
            Dimension(5.2, 1.0, 0.0), "1"
        )
        image_value.get_json()
        # TODO add image value json generation test


class TestRequestsImageMetaData(unittest.TestCase):
    """
    Unit testing for ImageMetaData class in requests module.

    """
    def test_init_image_meta_data(self):
        """
        Test generation of image meta data class
        """
        image_value = ImageValue(
            "test001.png", "1516193959559", Position(44.2, 17.4, 0.0),
            Dimension(5.2, 1.0, 0.0), "1"
        )
        image_value_list = [
            image_value,
            image_value
        ]
        qualifying_metadata = [
            {
                "key": "xxx",
                "value": "1"
            },
            {
                "key": "yyy",
                "value": "2"
            }
        ]
        image_meta_data = ImageMetaData(
            "Part1234", "Camera1", "I3DR_DESKTOP_ABC123",
            image_value_list, qualifying_metadata
        )

    def test_image_meta_data_json(self):
        """
        Tests image meta data json generation.

        """
        image_value = ImageValue(
            "test001.png", "1516193959559", Position(44.2, 17.4, 0.0),
            Dimension(5.2, 1.0, 0.0), "1"
        )
        image_value_list = [
            image_value,
            image_value
        ]
        qualifying_metadata = [
            {
                "key": "xxx",
                "value": "1"
            },
            {
                "key": "yyy",
                "value": "2"
            }
        ]
        image_meta_data = ImageMetaData(
            "Part1234", "Camera1", "I3DR_DESKTOP_ABC123",
            image_value_list, qualifying_metadata
        )
        image_meta_data.get_json()
        # TODO add image meta data json generation test


class TestRequestsImageAnalysisFailure(unittest.TestCase):
    """
    Unit testing for ImageAnalysisFailure class in requests module.

    """
    def test_init_image_analysis_failure(self):
        """
        Test generation of image analysis failure class
        """
        qualifying_metadata = [
            {
                "key": "xxx",
                "value": "1"
            },
            {
                "key": "yyy",
                "value": "2"
            }
        ]
        image_analysis_failure = ImageAnalysisFailure(
            "124355435321576", "4711", Position(44.2, 17.4, 0.0),
            Dimension(5.2, 1.0, 0.0), qualifying_metadata
        )

    def test_image_analysis_failure_json(self):
        """
        Tests image analysis failure json generation.

        """
        qualifying_metadata = [
            {
                "key": "xxx",
                "value": "1"
            },
            {
                "key": "yyy",
                "value": "2"
            }
        ]
        image_analysis_failure = ImageAnalysisFailure(
            "124355435321576", "4711", Position(44.2, 17.4, 0.0),
            Dimension(5.2, 1.0, 0.0), qualifying_metadata
        )
        image_analysis_failure.get_json()
        # TODO add image analysis failure json generation test


class TestRequestsImageAnalysisData(unittest.TestCase):
    """
    Unit testing for ImageAnalysisData class in requests module.

    """
    def test_init_image_analysis_data(self):
        """
        Test generation of image analysis data class
        """
        qualifying_metadata = [
            {
                "key": "xxx",
                "value": "1"
            },
            {
                "key": "yyy",
                "value": "2"
            }
        ]
        image_analysis_failure = ImageAnalysisFailure(
            "124355435321576", "4711", Position(44.2, 17.4, 0.0),
            Dimension(5.2, 1.0, 0.0), qualifying_metadata
        )
        image_analysis_failure_list = [
            image_analysis_failure,
            image_analysis_failure
        ]
        image_analysis_data = ImageAnalysisData(
            "Part1234", "I3DR_DESKTOP_ABC123",
            "test001.png", "1516193959559", image_analysis_failure_list
        )

    def test_image_analysis_data_json(self):
        """
        Tests image analysis data json generation.

        """
        qualifying_metadata = [
            {
                "key": "xxx",
                "value": "1"
            },
            {
                "key": "yyy",
                "value": "2"
            }
        ]
        image_analysis_failure = ImageAnalysisFailure(
            "124355435321576", "4711", Position(44.2, 17.4, 0.0),
            Dimension(5.2, 1.0, 0.0), qualifying_metadata
        )
        image_analysis_failure_list = [
            image_analysis_failure,
            image_analysis_failure
        ]
        image_analysis_data = ImageAnalysisData(
            "Part1234", "I3DR_DESKTOP_ABC123",
            "test001.png", "1516193959559", image_analysis_failure_list
        )
        image_analysis_data.get_json()
        # TODO add image analysis data json generation test


class TestPartDataEndpoint(unittest.TestCase):
    """
    Unit testing part data in requests with mock server.

    """
    def setUp(self):
        self.server_name = "127.0.0.1:5000"
        self.app, self.api = create_app({'SERVER_NAME': self.server_name})
        self.app_thread = multiprocessing.Process(target=self.app.run)
        self.app_thread.start()
        # poll server to check it's ready for testing
        while True:
            try:
                requests.get("http://{}/".format(self.server_name), timeout=0.5)
                return
            except requests.exceptions.ConnectionError:
                pass

    def tearDown(self):
        self.app_thread.terminate()

    def test_part_data_get(self):
        url = "http://{}/api/image_analysis_data".format(self.server_name)
        image_analysis_data = ImageAnalysisData.get(url)
        self.assertIsNotNone(image_analysis_data)

    def test_part_data_post(self):
        url = "http://{}/api/image_analysis_data".format(self.server_name)
        qualifying_metadata = [
            {
                "key": "xxx",
                "value": "1"
            },
            {
                "key": "yyy",
                "value": "2"
            }
        ]
        image_analysis_failure = ImageAnalysisFailure(
            "124355435321576", "4711", Position(44.2, 17.4, 0.0),
            Dimension(5.2, 1.0, 0.0), qualifying_metadata
        )
        image_analysis_failure_list = [
            image_analysis_failure,
            image_analysis_failure
        ]
        image_analysis_data = ImageAnalysisData(
            "Part1234", "I3DR_DESKTOP_ABC123",
            "test001.png", "1516193959559", image_analysis_failure_list
        )
        resp = image_analysis_data.post(url)
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()