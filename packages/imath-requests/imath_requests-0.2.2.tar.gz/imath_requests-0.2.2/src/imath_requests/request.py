"""
request.py
====================================
Request handelling and data structures for interacting with iMath REST API
"""

from typing import Type
import requests
import base64
from abc import ABC, abstractmethod
from requests import Response


class RequestError(Exception):
    """Base class for other request exceptions"""
    pass


class ResponseError(RequestError):
    """Exception for bad response"""
    def __init__(self, response: Response):
        self.message = "Server responded with exception.\n"
        self.message += "Status Code: {}\n".format(response.status_code)
        json = response.json()
        if 'exceptionClass' in json and 'message' in json:
            self.message += "Exception: {}\n".format(json['exceptionClass'])
            self.message += "Message: {}\n".format(json['message'])
        else:
            self.message += "Description: {}".format(response.text)
        super().__init__(self.message)


class HttpRequestMethodNotSupportedError(ResponseError):
    """Exception for Http Request Method Not Supported"""
    @staticmethod
    def _server_class() -> str:
        return "org.springframework.web.HttpRequestMethodNotSupportedException"


class iMathResponseError(ResponseError):
    """Exception for bad response from iMath backend exceptions"""
    @staticmethod
    def _server_class_base() -> str:
        return "at.abf.research.imath.restbackend.exception"


class EntityExistsError(iMathResponseError):
    """Exception for entity already exists"""

    @staticmethod
    def _server_class() -> str:
        return \
            iMathResponseError._server_class_base() + ".EntityExistsException"


class DataRequest(ABC):

    @staticmethod
    def get_api_endpoint() -> str:
        return "part"

    @abstractmethod
    def to_json(self) -> dict:
        # MUST be implimented by child class
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def from_json():
        # MUST be implimented by child class
        raise NotImplementedError

    def __str__(self) -> str:
        return str(self.to_json())

    @staticmethod
    def generate_server_header(username, password):
        """
        Get header for iMath REST API.

        Parameters
        ----------
        username : str
            username for iMath REST API
        password : str
            password for iMath REST API

        Returns
        -------
        dict
            header for iMath REST API

        """
        auth_string = "{}:{}".format(username, password)
        auth_string_b64 = base64.b64encode(auth_string.encode()).decode()
        return {
            "Authorization": "Basic {}".format(auth_string_b64)
        }

    @classmethod
    def get_url(cls, ip: str) -> str:
        api_endpoint = cls.get_api_endpoint()
        return 'http://{}/imath-rest-backend/{}'.format(ip, api_endpoint)

    @staticmethod
    def _response_exception(resp: Response):
        json = resp.json()
        if 'exceptionClass' in json and 'message' in json:
            exception_class_name = json['exceptionClass']
            exceptions = [
                HttpRequestMethodNotSupportedError,
                EntityExistsError]
            for exception in exceptions:
                if exception_class_name == exception._server_class():
                    raise exception(resp)
        raise ResponseError(resp)

    def post(self, ip: str, username: str, password: str) -> None:
        data = self.to_json()
        url = self.__class__.get_url(ip)
        header = DataRequest.generate_server_header(username, password)
        resp = requests.post(url, json=[data], headers=header)
        status_code = resp.status_code
        if (100 <= status_code and status_code <= 399):
            return resp
        else:
            DataRequest._response_exception(resp)

    @classmethod
    def get(cls, ip: str, username: str, password: str):
        url = cls.get_url(ip)
        header = DataRequest.generate_server_header(username, password)
        res = requests.get(url, headers=header)
        status_code = res.status_code
        if (100 <= status_code and status_code <= 399):
            json = res.json()
            return cls.from_json(json)
        else:
            DataRequest._response_exception(res)


class PartProperty(DataRequest):
    """
    Part property helper class.

    Includes addition functions creating json
    data from part property for easy use in REST API.

    Attributes
    ----------
    property: str
        Name of part property
    value: str/int/float
        value of part property

    """

    __valid_types = [str, int, float]
    __type_names = ["string", "int", "float"]

    def __init__(
            self, property: str, value: any):
        """
        Part property construction.

        Parameters
        ----------
        property: str
            Name of meta data property
        value: str/int/float
            value of part property

        """
        self.property = property
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if (type(value) not in PartProperty.__valid_types):
            err_msg = "Invalid type for part property value. "
            err_msg += "MUST be str, int, or float."
            raise TypeError(err_msg)
        self._value = value
        iter = zip(PartProperty.__valid_types, PartProperty.__type_names)
        for valid_type, type_name in iter:
            if type(value) == valid_type:
                self.value_type = type_name
                break

    def to_json(self) -> dict:
        """
        Convert PartProperty into json string for use in REST API.

        Returns
        -------
        dict
            Json formatted string

        """
        return {
            "key": self.property,
            self.value_type: self.value
        }

    @staticmethod
    def from_json(json: dict) -> 'PartProperty':
        if 'key' not in json:
            raise ValueError("Invalid json for part property. Missing 'key'.")

        iter = zip(PartProperty.__valid_types, PartProperty.__type_names)
        for valid_types, type_name in iter:
            if type_name in json:
                return PartProperty(json['key'], valid_types(json[type_name]))


class PartData(DataRequest):
    """
    Part data helper class.

    Includes addition functions creating json
    data from part data for easy use in REST API.

    Attributes
    ----------
    identifiedTime: str
        Timestamp e.g. 1516193959559
    partId: str
        Unique part ID e.g. Part1234
    source: str
        Data source e.g. I3DR_DESKTOP_ABC123
    properties: list
        List of PartProperty. Additional part properties.

    """

    def __init__(
            self, identifiedTime: str, partId: str,
            source: str, properties: list):
        """
        Part construction.

        Parameters
        ----------
        identifiedTime: str
            Timestamp e.g. 1516193959559
        partId: str
            Unique part ID e.g. Part1234
        source: str
            Data source e.g. I3DR_DESKTOP_ABC123
        properties: list
            List of PartProperty. Additional part properties.

        """
        self.identifiedTime = identifiedTime
        self.partId = partId
        self.source = source
        self.properties = properties

    def to_json(self) -> dict:
        """
        Convert PartData into json string for use in REST API.

        Returns
        -------
        dict
            Json formatted string

        """
        props_json_list = []
        for prop in self.properties:
            props_json_list.append(prop.to_json())
        return {
            "identifiedTime": self.identifiedTime,
            "partId": self.partId,
            "source": self.source,
            "partData": props_json_list
        }

    @staticmethod
    def from_json(json: dict) -> 'PartData':
        valid_keys = ["identifiedTime", "partId", "source", "partData"]
        for key in valid_keys:
            if key not in json:
                raise ValueError(
                    "Invalid json for part data. Missing '{}'".format(key))
        props_json_list = json['partData']
        properties = []
        for prop_json in props_json_list:
            properties.append(
                PartProperty.from_json(prop_json))
        return PartData(
            json['identifiedTime'], json['partId'],
            json['source'], properties
        )


class Dimension:
    """
    Dimension helper class.

    Includes addition functions creating json data
    from part data for easy use in REST API.

    Attributes
    ----------
    x: float
        X-axis dimension
    y: float
        Y-axis dimension
    z: float
        Z-axis dimension

    """
    def __init__(self, x: float, y: float, z: float):
        """
        Dimension construction.

        Parameters
        ----------
        x: float
            X-axis dimension
        y: float
            Y-axis dimension
        z: float
            Z-axis dimension

        """
        self.x = x
        self.y = y
        self.z = z

    def to_json(self):
        """
        Convert Dimension into json string for use in REST API.

        Returns
        -------
        dict
            Json formatted string

        """
        return [
            self.x,
            self.y,
            self.z
        ]


class Position:
    """
    Position helper class.

    Includes addition functions creating json data
    from part data for easy use in REST API.

    Attributes
    ----------
    x: float
        X-axis position
    y: float
        Y-axis position
    z: float
        Z-axis position

    """
    def __init__(self, x: float, y: float, z: float):
        """
        Position construction.

        Parameters
        ----------
        x: float
            X-axis position
        y: float
            Y-axis position
        z: float
            Z-axis position

        """
        self.x = x
        self.y = y
        self.z = z

    def to_json(self):
        """
        Convert Position into json string for use in REST API.

        Returns
        -------
        dict
            Json formatted string

        """
        return [
            self.x,
            self.y,
            self.z
        ]


class ImageData:
    """
    Image Data helper class.

    Includes addition functions creating json data
    from part data for easy use in REST API.

    Attributes
    ----------
    filename: str
        Name of the image e.g. test001.png
    timestamp: str
        Timestamp e.g. 1516193959559
    position: Position
        Position on the part where the image was taken
    dimension: Dimension
        Dimension of the area of the part, which is on the image
    quality: str
        Quality

    """

    def __init__(
            self, filename: str, timestamp: str,
            position: Position, dimension: Dimension, quality: str):
        """
        Image data construction.

        Parameters
        ----------
        filename: str
            Name of the image e.g. test001.png
        timestamp: str
            Timestamp e.g. 1516193959559
        position: str
            Position on the part where the image was taken
        dimension: str
            Dimension of the area of the part, which is on the image
        quality : str
            Quality

        """
        self.filename = filename
        self.timestamp = timestamp
        self.position = position
        self.dimension = dimension
        self.quality = quality

    def to_json(self) -> dict:
        """
        Convert ImageData into json string for use in REST API.

        Returns
        -------
        dict
            Json formatted string

        """
        return {
            "filename": self.filename,
            "timestamp": self.timestamp,
            "position": self.position.to_json(),
            "dimension": self.dimension.to_json(),
            "quality": self.quality
        }


class ImageMetaData:
    """
    Image meta data helper class.

    Includes addition functions creating json data
    from image meta data for easy use in REST API.

    Attributes
    ----------
    part_id: str
        Unique part ID e.g. Part1234
    captured_by: str
        Unique identification of the capture device e.g. Camera1
    source: str
        Data source e.g. I3DR_DESKTOP_ABC123
    images: list
        List of ImageData
    qualifying_metadata: list
        Qualifying metadata should be a key value pair array

    """

    def __init__(
            self, part_id: str, captured_by: str,
            source: str, values: list, qualifying_metadata):
        """
        Image meta data construction.

        Parameters
        ----------
        part_id: str
            Unique part ID e.g. Part1234
        captured_by: str
            Unique identification of the capture device e.g. Camera1
        source: str
            Data source e.g. I3DR_DESKTOP_ABC123
        values: list
            List of ImageValues
        qualifying_metadata: list
            Qualifying metadata should be a key value pair array

        """
        self.part_id = part_id
        self.captured_by = captured_by
        self.source = source
        self.values = values
        self.qualifying_metadata = qualifying_metadata

    def to_json(self) -> dict:
        """
        Convert ImageMetaData into json string for use in REST API.

        Returns
        -------
        dict
            Json formatted string

        """
        values_json_list = []
        for value in self.values:
            values_json_list.append(value.to_json())
        return {
            "part_id": self.part_id,
            "captured_by": self.captured_by,
            "source": self.source,
            "values": values_json_list,
            "qualifying_metadata": self.qualifying_metadata
        }


class ImageAnalysisDefect:
    """
    Image analysis defect helper class.

    Includes addition functions creating json data
    from part data for easy use in REST API.

    Attributes
    ----------
    id: str
        Unique defect id e.g. 124355435321576
    defect_type_id: str
        defect type id e.g. 4711
    position: Position
        Position on the part where the image was taken
    dimension: Dimension
        Dimension of the area of the part, which is on the image
    qualifying_metadata: list
        Qualifying metadata should be a key value pair array

    """
    def __init__(
            self, id: str, defect_type_id: str,
            position: Position, dimension: Dimension,
            qualifying_metadata: list):
        """
        Image analysis defect construction.

        Parameters
        ----------
        id: str
            Unique defect id e.g. 124355435321576
        defect_type_id: str
            defect type id e.g. 4711
        position: Position
            Position on the part where the image was taken
        dimension: Dimension
            Dimension of the area of the part, which is on the image
        qualifying_metadata: list
            Qualifying metadata should be a key value pair array

        """
        self.id = id
        self.defect_type_id = defect_type_id
        self.position = position
        self.dimension = dimension
        self.qualifying_metadata = qualifying_metadata

    def to_json(self) -> dict:
        """
        Convert ImageAnalysisDefect into json string for use in REST API.

        Returns
        -------
        dict
            Json formatted string

        """
        return {
            "id": self.id,
            "defect_type_id": self.defect_type_id,
            "position": self.position.to_json(),
            "dimension": self.dimension.to_json(),
            "qualifying_metadata": self.qualifying_metadata
        }


class ImageAnalysisData(DataRequest):
    """
    Image analysis data helper class.

    Includes addition functions creating json data
    from image analysis data for easy use in REST API.

    Attributes
    ----------
    part_id : str
        Unique part ID e.g. Part1234
    source : str
        Data source e.g. I3DR_DESKTOP_ABC123
    value: list
        List of ImageData
    timestamp : str
        Timestamp e.g. 1516193959559
    defects: list
        list of ImageAnalysisDefect

    """

    def __init__(
            self, part_id: str, source: str,
            value: list, timestamp: str, defects: list):
        """
        Image Meta Data construction.

        Parameters
        ----------
        part_id : str
            Unique part ID e.g. Part1234
        source : str
            Data source e.g. I3DR_DESKTOP_ABC123
        value: str
            Name of the image (NOT ImageValue)
        timestamp : str
            Timestamp e.g. 1516193959559
        defects: list
            list of ImageAnalysisDefect

        """
        self.part_id = part_id
        self.source = source
        self.value = value
        self.timestamp = timestamp
        self.defects = defects

    def to_json(self) -> dict:
        """
        Convert ImageAnalysisData into json string for use in REST API.

        Returns
        -------
        dict
            Json formatted string

        """
        defects_json_list = []
        for defect in self.defects:
            defects_json_list.append(defect.to_json())
        return {
            "part_id": self.part_id,
            "source": self.source,
            "value": self.value,
            "timestamp": self.timestamp,
            "defects": defects_json_list
        }

    @staticmethod
    def from_json(json: str) -> 'ImageAnalysisData':
        part_id = json['part_id']
        source = json['source']
        value = json['value']
        timestamp = json['timestamp']
        defects = []
        for defect in json['defects']:
            position = Position(
                defect['position'][0],
                defect['position'][1],
                defect['position'][2])
            dimension = Dimension(
                defect['dimension'][0],
                defect['dimension'][1],
                defect['dimension'][2])
            defects.append(
                ImageAnalysisDefect(
                    defect['id'], defect['defect_type_id'], position,
                    dimension, defect['qualifying_metadata']
                )
            )
        return ImageAnalysisData(
            part_id, source, value, timestamp, defects)


if __name__ == "__main__":
    import os

    if 'IMATH_SERVER_IP' in os.environ:
        server_ip = os.environ['IMATH_SERVER_IP']
    else:
        server_ip = '127.0.0.1:5000'
    if 'IMATH_USERNAME' in os.environ:
        server_username = os.environ['IMATH_USERNAME']
    else:
        server_username = 'test'
    if 'IMATH_PASSWORD' in os.environ:
        server_password = os.environ['IMATH_PASSWORD']
    else:
        server_password = 'test'

    part = PartData(
        '1516193959559', 'Part43211', 'I3DR_DESKTOP_ABC123',
        [
            PartProperty("Steel grade", "Grade01")
        ]
    )
    resp = part.post(server_ip, server_username, server_password)
    print(resp)
