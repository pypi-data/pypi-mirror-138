#!/usr/bin/env python3
"""
Purpose:        A library to access the LOGS API via Python
Python Version: Python 3.8 and above
Disclaimer:     This script is provided "as is" by Signals GmbH & KO KG to demostrate 
                the functionality of the LOGS API
License:        MIT License

When              Version       Who               What
-----------------------------------------------------------------------------------------
2021-07-16        0.1           Sina Kazemi       First version
-----------------------------------------------------------------------------------------
"""

# import json
from typing import List, Tuple, Union
import requests
import regex as re
from urllib.parse import parse_qs, urlparse
import json


class LOGSAPI:
    """Python class to access the LOGS web API"""

    __url_re = re.compile(r"(?:(https*)\:\/\/)*([^\/:]+)(?:\:(\d+))*(?:\/(.*))*")
    __url_api_re = re.compile(r"api\/(\d+\.\d+)")
    __byteUnits = ["", "K", "M", "G", "T", "P", "E", "Z"]

    def __init__(self, url: str, api_key: str, use_internal: bool = False, verbose: bool = False):
        """Checks the connection to the server on creation

        Args:
            url (str): URL to specific LOGS group (e.g. https://mylogs/mygroup or https://mylogs:80/mygroup/api/0.1)
            api_key (str): The API key that grants access to LOGS (you need to generate on in LOGS and copy it)
            verbose (bool, optional): If set you see some information about the server connection. Defaults to False.

        Raises:
            Exception: URL must does not defined or is invalid.
            Exception: The URL does not define a group.
            Exception: Server cannot be reached.
        """
        match = self.__url_re.search(url)
        protocol = "http"
        version = "0.1"
        if not match:
            raise Exception("Invalid URL '%s'." % url)
        else:
            (protocol, server, port, endpoints) = match.groups()
            if endpoints:
                group = endpoints.split("/")[0]
            else:
                group = None
            if server == None or server == "":
                raise Exception("URL must define a server.")
            if group == None or group == "":
                raise Exception("URL must cotain a group.")

            if port == "":
                port = None

            match = self.__url_api_re.search(endpoints)
            if match:
                version = match.group(1)

        # print("match", (protocol, server, port, group, version))

        self.promptPrefix = "LOGSAPI>"
        self.verbose = verbose

        self.__version = version
        self.__protocol = protocol
        self.__server = server
        self.__port = port
        self.__group = group
        if self.verbose:
            print(self.promptPrefix, "Server properties:")
            print(self.promptPrefix, "   protocol:", self.__protocol)
            print(self.promptPrefix, "   server:", self.__server)
            print(self.promptPrefix, "   port:", self.__port)
            print(self.promptPrefix, "   group:", self.__group)

        self.__requestHistory = []

        self.__api_key = api_key
        self.__group = group
        self.__logsURL = url
        self.__useInternal = use_internal

        self.checkServer()

    @property
    def version(self) -> str:
        return self.__version

    @property
    def protocol(self):

        return self.__protocol

    @property
    def server(self) -> str:
        return self.__server

    @property
    def port(self) -> int:
        return self.__port

    @property
    def group(self) -> str:
        return self.__group

    @property
    def api_key(self) -> str:
        return self.__api_key

    def getAPIUrl(self) -> str:
        """Generate full API URL

        Returns:
            str: The url of the connected LOGS API (e.g. https://logs.com/api/2.1)
        """
        return "%s://%s%s/%s/api/%s" % (
            self.protocol,
            self.server,
            ":" + self.port if self.port else "",
            self.group,
            self.version,
        )

    @classmethod
    def getHumanReadableSize(cls, size, suffix="B"):
        for unit in cls.__byteUnits:
            if abs(size) < 1024.0:
                return "%3.1f%s%s" % (size, unit, suffix)
            size /= 1024.0
        return "%.1f%s%s" % (size, "Yi", suffix)

    def getNextPage(self, result):
        # print("response", result["url"])
        # o = urlparse(result["url"])
        # params = parse_qs(o.query)

        # if "Page" in params:
        #     # print("Page", int(params["Page"][0]))
        #     params["Page"][0] = int(params["Page"][0]) + 1
        # else:
        #     params["Page"] = 2
        # url = "%s://%s%s" % (o.scheme, o.netloc, o.path)

        params = None
        url = result["next"]
        # print(f"next page '{url}'")
        if not url:
            return None, None
        return self.getUrl(url, params)

    def getEndpointUrl(self, endpoint: Union[str, List[str]]) -> str:
        """Generate full API URL for a given endpoint

        Returns:
            str: The url of the connected LOGS API (for dataset endpoint e.g. https://logs.com/api/2.1/dataset)
        """

        if isinstance(endpoint, list):
            endpoint = "/".join([str(e) for e in endpoint])

        return self.getAPIUrl() + "/" + endpoint

    def getUrl(
        self, url: str = None, params: dict = None, mode: str = "json", return_url: bool = True
    ) -> Tuple[str, str]:
        """Generate full API URL with GET parameters

        Args:
            url (str, optional): Specify an API url otherwise object internal is used. Defaults to None.
            params (dict, optional): Parameters to pass to an GET request. Defaults to None.
            mode (str, optional): The return value is converted to the specified format. Defaults to "json".

        Returns:
            (str, str): The respose of the server and the error code.
        """
        if self.verbose:
            print(self.promptPrefix, "GET: %s" % url)

        # print("params", params)
        response = requests.get(url, headers=self.getHeader(), params=params)

        # if response == None:
        #     response =
        # print("url", url)
        return self.__convertResponse(response, mode, return_url)

    def getHeader(self):
        if self.__useInternal:
            return {"X-Api-Key": self.api_key, "X-LOGS-internal": "true"}
        else:
            return {"X-Api-Key": self.api_key}

    def deleteUrl(self, url: str = None, params: dict = {}, mode: str = "json") -> Tuple[str, str]:
        """Generate full API URL with PUT body

        Args:
            url (str, optional): Specify an API url otherwise object internal is used. Defaults to None.
            params (dict, optional): Parameters to pass to an PUT request as json body. Defaults to None.
            mode (str, optional): The return value is converted to the specified format. Defaults to "json".

        Returns:
            (str, str): The respose of the server and the error code.
        """

        if self.verbose:
            print(self.promptPrefix, "DELETE: %s" % url)

        response = requests.delete(url, headers=self.getHeader(), json=params)
        return self.__convertResponse(response, mode)

    def putUrl(self, url: str = None, params: dict = {}, mode: str = "json") -> Tuple[str, str]:
        """Generate full API URL with PUT body

        Args:
            url (str, optional): Specify an API url otherwise object internal is used. Defaults to None.
            params (dict, optional): Parameters to pass to an PUT request as json body. Defaults to None.
            mode (str, optional): The return value is converted to the specified format. Defaults to "json".

        Returns:
            (str, str): The respose of the server and the error code.
        """

        if self.verbose:
            print(self.promptPrefix, "PUT: %s" % url)

        response = requests.put(url, headers=self.getHeader(), json=params)
        return self.__convertResponse(response, mode)

    def putEndpoint(self, endpoint: Union[str, List[str]], params: dict = None, mode: str = "json") -> Tuple[str, str]:
        """Connects to the API with PUT access to given endpoint

        Args:
            endpoint (str): Name of the endpoint (e.g. dataset/2/tracks)
            params (str, optional): Parameters to pass to the endpoint as json body. Defaults to None.

        Returns:
            (str, str): The respose of the server and the error code.
        """
        url = self.getEndpointUrl(endpoint)

        return self.putUrl(url, params, mode)

    def postUrl(self, url: str = None, params: dict = {}, mode: str = "json") -> Tuple[str, str]:
        """Generate full API URL with PUT body

        Args:
            url (str, optional): Specify an API url otherwise object internal is used. Defaults to None.
            params (dict, optional): Parameters to pass to an PUT request as json body. Defaults to None.
            mode (str, optional): The return value is converted to the specified format. Defaults to "json".

        Returns:
            (str, str): The respose of the server and the error code.
        """

        if self.verbose:
            print(self.promptPrefix, "POST: %s" % url)

        response = requests.post(url, headers=self.getHeader(), json=params)
        return self.__convertResponse(response, mode)

    def postEndpoint(self, endpoint: Union[str, List[str]], params: dict = None, mode: str = "json") -> Tuple[str, str]:
        """Connects to the API with PUT access to given endpoint

        Args:
            endpoint (str): Name of the endpoint (e.g. dataset/2/tracks)
            params (str, optional): Parameters to pass to the endpoint as json body. Defaults to None.

        Returns:
            (str, str): The respose of the server and the error code.
        """
        url = self.getEndpointUrl(endpoint)

        return self.postUrl(url, params, mode)

    def deleteEndpoint(
        self, endpoint: Union[str, List[str]], params: dict = None, mode: str = "json"
    ) -> Tuple[str, str]:
        """Connects to the API with PUT access to given endpoint

        Args:
            endpoint (str): Name of the endpoint (e.g. dataset/2/tracks)
            params (str, optional): Parameters to pass to the endpoint as json body. Defaults to None.

        Returns:
            (str, str): The respose of the server and the error code.
        """
        url = self.getEndpointUrl(endpoint)

        return self.deleteUrl(url, params=params, mode=mode)

    def getEndpoint(
        self, endpoint: Union[str, List[str]], params: dict = None, mode: str = None, return_url: bool = True
    ) -> Tuple[str, str]:
        """Connects to the API with GET access to given endpoint

        Args:
            endpoint (str): Name of the endpoint (e.g. dataset/2/tracks)
            params (str, optional): Parameters to pass to the endpoint. Defaults to None.
            mode (str, optional): Convert result to this format. Defaults to None.

        Returns:
            (str, str): The respose of the server and the error code.
        """
        # print("Headers:", headers)
        # print("Params:", params)
        url = self.getEndpointUrl(endpoint)

        return self.getUrl(url, params=params, mode=mode, return_url=return_url)

        # header = {"X-Api-Key": api_key}

        # # try:
        # response = requests.get(url, headers=header, params=params, verify=False)
        # # except ValueError as error:
        # #     print(error)
        # return self.convertResponse(response, mode)

    def convertCustomFieldParams(self, params: dict):

        # print(">", params)
        return {"customFields[%s]" % k: v for k, v in params.items()}

    def __convertResponse(self, response, mode: str = "json", return_url: bool = True):
        if response.status_code == 200:
            if mode == "raw":
                return response.content, None
            else:
                result = response.json()
                if isinstance(result, dict) and return_url:
                    result["url"] = response.url
                return result, None
        else:
            error = ""
            try:
                r = response.json()
                if "error" in r:
                    error = " (%s)" % r["error"]

                if "errors" in r:
                    # print(">>", r["errors"].items())
                    errors = []
                    for k, v in r["errors"].items():
                        errors.append(k + ": " + " ".join(v) if isinstance(v, list) else str(v))
                    if error != "":
                        error += "\n"
                    error += "\n".join(errors)
            except:
                pass

            if error != "":
                error = ", " + error
            return (
                response,
                # str(response.status_code) + " " + response.reason + error
                str(response.status_code) + " " + response.reason + error
                if response.status_code != 204
                else "",  # exclude code 204 for now
            )

    def checkServer(self):
        """Check if server can be reached

        Raises:
            Exception: Server cannot be reached.
        """
        testEndpoint = "version"

        result, error = self.getEndpoint(testEndpoint)
        if error:
            raise Exception("Could not connect to '%s': %s" % (result.url, error))
        if self.verbose:
            print(
                self.promptPrefix,
                "Connection to server '%s://%s%s' successful."
                % (self.protocol, self.server, ":" + self.port if self.port else ""),
            )

    @classmethod
    def __checkParams(cls, params: dict):
        p = {}

        mustBePositiveInt = {"id", "operatorId", "projectId", "documentId", "sampleId", "page", "pageSize"}

        for k, v in params.items():
            if v == None:
                continue
            if k in mustBePositiveInt:
                if not isinstance(v, int):
                    raise Exception("Parameter '%s' must be of type int. (Got '%s')" % (k, type(v).__name__))
                if v < 0:
                    raise Exception("Parameter '%s' must be zero or positive. (Got '%d')" % (k, v))

            p[k] = v

        if "customFields" in params and params["customFields"] != None:
            del p["customFields"]
            k, v = "customFields", params["customFields"]
            if not isinstance(v, dict):
                raise Exception("Parameter '%s' must be of type dict. (Got '%s')" % (k, type(v).__name__))
            custom = []
            for k, v in params["customFields"].items():
                custom.append(k + ":" + str(v))
                print(k, v)
            p["custom"] = custom

        return p


if __name__ == "__main__":
    api_key = input("Please specify api key: ")
    url = input("Please specify LOGS url: ")

    # Example input:
    # api_key = "8V6oQ804t2nPgGPDJIk4CuneRI5q48ERUxgEpk+YqXzX9uLuMUySycHkeXP6DefN"
    # url = "http://localhost:900/sandbox"

    logs = LOGSAPI(url, api_key, verbose=True)
