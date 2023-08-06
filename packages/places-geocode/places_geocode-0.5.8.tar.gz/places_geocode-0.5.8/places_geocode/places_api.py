import time
from typing import Any, List, Optional, Callable, Union
from fastapi import UploadFile
from requests import get, post
from requests.exceptions import HTTPError, Timeout
from pydantic import BaseModel
import aiohttp
from abc import ABC, abstractmethod
# noinspection PyCompatibility
import asyncio
import json
# noinspection PyCompatibility
import urllib.request as url_request
# noinspection PyCompatibility
import urllib.parse as url_parse
from time import perf_counter


# model for settings
# noinspection PyCompatibility
class GlobalCallSettings(BaseModel):
    """base model for settings calls"""
    protocol: Optional[str] = 'requests'
    reverse_model: Optional[str] = 'roof_top'
    geocode_model: Optional[str] = 'roof_top'
    density_model: Optional[str] = '2dSphere'
    timeout_len: Optional[float] = 5.0


# utilities class
# noinspection PyCompatibility
class Utilities:

    def __init__(self):
        self.name = 'util'

    @staticmethod
    def coords_conv(coordinates) -> List[list]:
        """convert coordinates to lats and longs"""

        # create containers for lats and longs
        lats: list = []
        longs: list = []

        # separate the latitudes and longitudes
        [(lats.append(i[0]), longs.append(i[1])) for i in coordinates]

        return [lats, longs]


# implement strategy pattern for request call protocols
class ProtocolStrategy(ABC):
    """protocol abstract base class for strategy implementation"""

    @abstractmethod
    def call_protocol(self, response: Callable, method: str, payload, **kwargs) -> Any:
        pass


class BasicRequest(ProtocolStrategy):
    """basic requests"""

    def call_protocol(self, response: Callable, method: str, payload, **kwargs) -> Any:
        return response(method, payload, **kwargs)


# noinspection PyTypeChecker
class AIORequest(ProtocolStrategy):
    """run the asynchronous request for aiohttp protocol"""

    def call_protocol(self, response: Callable, method: str, payload, **kwargs) -> Any:

        return asyncio.run(response(payload, **kwargs))


class URLLIBRequest(ProtocolStrategy):
    """urllib reader protocol processor"""

    def call_protocol(self, response: Callable, method: str, payload, **kwargs) -> Any:
        return json.loads(response(payload, **kwargs))


# strategy pattern for package middlewares
class Middleware(ABC):
    """middleware for places geocoding plans"""

    @abstractmethod
    def middleware_call(self) -> Any:
        pass


# strategy pattern for free plan
class FreeMiddlware(Middleware):
    """free plan middleware strategy -> wait 0.5 seconds (2 requests / second)"""

    def middleware_call(self) -> Any:
        """2 requests per second"""
        time.sleep(0.5)


# noinspection PyCompatibility
class Places(Utilities):
    """places facade class for package contents"""

    def __init__(self, token: str = "free"):
        # get base model for global states
        super().__init__()
        self.global_model: GlobalCallSettings = GlobalCallSettings()

        # access token
        self.token: str = token

        # create middleware instances
        self.middlewares: dict = {"free": FreeMiddlware()}
        try:
            self.middlewares[self.token.lower()].middleware_call()
            self.token: str = 'k9ppk3WunSAr'
            print("Called Middlware")
        except KeyError:
            pass


        # base url for places geocoding server
        self.url_mapping: dict = {
            1: f'https://places-api-dob9z.ondigitalocean.app/xxx/{self.global_model.reverse_model}',
            2: f'https://places-api-dob9z.ondigitalocean.app/xxx/{self.global_model.density_model}',
            3: f'https://places-api-dob9z.ondigitalocean.app/xxx/{"reverse_model"}/',
            4: f'https://places-api-dob9z.ondigitalocean.app/xxx/{"{reverse_model}"}',
            5: f'https://places-api-dob9z.ondigitalocean.app/xxx/{"{geocode_model}"}'}

        # create mapping for caller and protocols
        protocol_mapping: dict = {'requests': (BasicRequest(), self._call_url_requests),
                                  'aiohttp': (AIORequest(), self._call_url_aiohttp),
                                  'urllib': (URLLIBRequest(), self._call_url_urllib)}
        # unpack the strategies
        self.proto_runner, self.call_runner = protocol_mapping[self.global_model.protocol]

    @staticmethod
    def _unpack_runtime(runtime: dict):
        """unpack the runtime type"""
        # get the type of request to be made
        try:
            request_type: int = runtime['type']
        except KeyError:
            request_type: int = 1

        return request_type

    def _call_url_requests(self, method: str, payload: dict, **runtime):
        """call the url with requests library"""

        # get the type of request to be made
        request_type = self._unpack_runtime(runtime)
        try:
            proto: Callable = runtime['proto']
        except KeyError:
            raise Exception('404: <No Callable Protocol Selected>')

        # format REST API url
        rest_url: str = self.url_mapping[request_type].replace('xxx', method)

        # send request
        try:
            result = proto(rest_url, params=payload, timeout=self.global_model.timeout_len)#.json()
            return result.json()
        except (HTTPError, TimeoutError, Timeout):
            raise Exception("404: <Places Server in Timeout. Attempt Blocked>")

    async def _call_url_aiohttp(self, method, payload: dict, **runtime):
        """call url with aiohttp library"""

        # get the type of request to be made
        request_type = self._unpack_runtime(runtime)
        try:
            proto: Union[Callable, str] = runtime['proto']
        except KeyError:
            raise Exception('404: <No Callable Protocol Selected>')

        # crete REST API url
        rest_url: str = self.url_mapping[request_type].replace('xxx', method)

        # make asynchronous request
        if proto == 'get':
            async with aiohttp.ClientSession() as session:
                async with session.get(rest_url, params=payload) as resp:
                    response = await resp.json()
        elif proto == 'post':
            async with aiohttp.ClientSession() as session:
                async with session.post(rest_url, data=payload) as resp:
                    response = await resp.json()

        return response

    def _call_url_urllib(self, payload: dict, **runtime):
        """urllib caller function"""

        # get the request type
        request_type = self._unpack_runtime(runtime)

        # encode the parameters
        query_string: str = url_parse.urlencode(payload)
        url: str = self.url_mapping[request_type] + "?" + query_string

        # make request to server
        with url_request.urlopen(url) as response:
            return response.read()

    @staticmethod
    def process_basic_args(additional_args: dict) -> bool:
        """process the basic arguments for load radius, convex, density, reverse, and batch reverse methods"""

        # reverse_parameter extraction
        try:
            reverse_param: Any = additional_args['reverse_param']
        except KeyError:
            reverse_param: Any = None

        return reverse_param

    def load_properties(self, coordinates: list = (), radius: Any = 10, **additional):
        """load properties facade for package purposes"""

        # get token and reverse parameter
        reverse_param = self.process_basic_args(additional)
        payload: dict = {"latitude": coordinates[0], 'longitude': coordinates[1], "radius": radius, "token": self.token,
                         'reverse_param': reverse_param}

        # create and send response package
        return self.proto_runner.call_protocol(self.call_runner, 'load_properties_api', payload, type=1, proto=get)

    def convex(self, coordinates: list, **additionals) -> Any:
        """convex search facade method for places package"""

        # get token and reverse parameter
        reverse_param = self.process_basic_args(additionals)

        # split lats and long into arrays
        latitudes, longitudes = self.coords_conv(coordinates)
        payload: dict = {"latitudes": latitudes, "longitudes": longitudes, "reverse_param": reverse_param,
                         "token": self.token}

        # create response and send it
        return self.proto_runner.call_protocol(self.call_runner, 'convex_search', payload, type=1, proto=get)

    def density(self, unit_in="ft", unit_out="ft", coordinates: list = None, radius: Any = 1,
                custom_option: str = None, custom_utility: Any = None, **additionals) -> Any:
        """density facade function for places package"""

        # get token and reverse parameter
        reverse_param = self.process_basic_args(additionals)

        # get coordinates for query
        try:
            latitude, longitude = coordinates[0], coordinates[1]
        except (IndexError, TypeError):
            latitude, longitude = None, None

        # create payload package
        payload: dict = {"token": self.token, "latitude": latitude, "longitude": longitude,
                         "unit_in": unit_in, "unit_out": unit_out, "radius": radius, "reverse_param": reverse_param,
                         "custom_option": custom_option, "custom_utility": custom_utility}

        return self.proto_runner.call_protocol(self.call_runner, 'density_search', payload, type=2, proto=get)

    def reverse(self, coordinate: list = (), radius: Any = 10, **additionals) -> Any:
        """reverse geocoding facade method for Places package"""

        # get token and reverse parameter
        reverse_param = self.process_basic_args(additionals)
        payload: dict = {"token": self.token, "latitude": coordinate[0], "longitude": coordinate[1], "radius": radius,
                         "reverse_param": reverse_param, 'search_model': self.global_model.reverse_model}

        # create and send response packet
        return self.proto_runner.call_protocol(self.call_runner, "reverse_geocode", payload, type=3, proto=get)

    def batch_reverse(self, coordinates: List[list] = (()), radius: Any = 10, coordinate_file: UploadFile = None,
                      **additionals) -> Any:
        """batch reverse geocoding facade method for Places package"""

        # get token and reverse parameter
        reverse_param = self.process_basic_args(additionals)

        # create containers for lats and longs
        latitudes, longitudes = self.coords_conv(coordinates)

        # create request payload
        payload: dict = {"token": self.token, "latitudes": latitudes, "longitudes": longitudes, "radius": radius,
                         "coordinate_file": coordinate_file, "reverse_param": reverse_param,
                         'search_model': self.global_model.reverse_model}

        # create and send response packet
        return self.proto_runner.call_protocol(self.call_runner, "batch_reverse", payload, type=4, proto=post)

    def forward(self, full_address: str = None, street: str = None, number: Any = None, postcode: int = None,
                region: str = None, city: str = None, unit=None) -> Any:
        """facade method for forward geocoding on Places API"""

        # create payload
        payload: dict = {"token": self.token, "full_address": full_address, "street": street, "number": number,
                         "postcode": postcode, "region": region, "city": city, "unit": unit,
                         "search_model": self.global_model.geocode_model}

        return self.proto_runner.call_protocol(self.call_runner, "geocode", payload, type=5, proto=get)

    def batch_forward(self, addresses: list = (), address_file: UploadFile = None) -> Any:
        """batch forward facade method"""

        # create request payload
        payload: dict = {"token": self.token, "addresses": addresses, "address_file": address_file,
                         'search_model': self.global_model.geocode_model}

        # send response
        return self.proto_runner.call_protocol(self.call_runner, "batch_geocode", payload, type=5, proto=post)

