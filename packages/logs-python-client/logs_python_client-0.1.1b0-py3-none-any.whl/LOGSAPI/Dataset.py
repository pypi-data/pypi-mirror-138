import re
from LOGSAPI.Track import Track
from LOGSAPI.Sample import Sample
from LOGSAPI.Instrument import Instrument
from typing import Callable, List, Optional, Tuple
from datetime import datetime
import json


class Dataset:
    """Represents a LOGS dataset"""

    tracks: Optional[List[Track]]

    def __init__(self, data: dict, getUrl: Callable[[str], Tuple[str, str]] = None, formatValues: bool = True):
        """Create a dataset from a dictionary

        Args:
            data (dict): Dictionary representing the dataset (e.g. from a LOGS web API response)
            getUrl (Callable, optional): A function to retrive the full dataset. Defaults to None.
        """
        # print("Dataset", formatValues)
        self.__parameter = None
        self.formatValues = formatValues

        self.getUrl = getUrl
        self.init(data)

    def init(self, data: dict):
        self.id = data["id"] if "id" in data else None
        self.method = data["method"]["name"] if "method" in data else None
        self.sample = Sample(data["sample"]) if "sample" in data else None
        self.custom = data["custom"] if "custom" in data else None
        self.path = data["path"] if "path" in data else None
        self.acquisitionDate = data["acquisitionDate"] if "acquisitionDate" in data else None
        self.notes = data["notes"] if "notes" in data else None
        self.operators = data["operators"] if "operators" in data else None
        self.projects = data["projects"] if "projects" in data else None
        self.documents = data["documents"] if "documents" in data else None
        self.zip = data["zip"] if "zip" in data else None
        self.instrument = Instrument(data["instrument"], self.getUrl) if "instrument" in data else None
        self.experiment = data["experiment"] if "experiment" in data else None
        self.type = data["type"] if "type" in data else None
        self.url = data["url"] if "url" in data else None

        self.__parameter = data["parameter"] if "parameter" in data else None

        if self.acquisitionDate:

            d = self.acquisitionDate.split(".")
            if len(d) > 1:
                match = re.match(r"(\d+)([\+\-].*)", d[1])
                if match and len(match.group(1)) < 3:  # python isoformat does not accept ms with less than 3 positions
                    self.acquisitionDate = d[0] + "." + match.group(1).zfill(6) + match.group(2)

            try:
                # self.acquisitionDate = datetime.strptime(self.acquisitionDate, "%Y-%m-%dT%H:%M:%S.%f+%z")
                self.acquisitionDate = datetime.fromisoformat(self.acquisitionDate)
            except Exception as e:
                self.acquisitionDate = None

        if "tracks" in data and data["tracks"] != None:
            self.tracks = list(map(lambda d: Track(d, self.getUrl), data["tracks"]))
        else:
            self.tracks = None

        # if "shape" in data:
        #     self.__shape = data["shape"]

    @property
    def parameters(self) -> Optional[dict]:
        """The dataset parameters. Will make a API call if parameter is not set.

        Returns:
            dict: The formatted parameters of this dataset
        """
        # print("get parameters", self.__parameter)
        if not self.__parameter:
            self.getFullDataset()

        if self.__parameter == None:
            return {}
        return self.__parameter

    @property
    def trackNames(self) -> List[str]:
        """Returns the list of track names of this dataset

        Returns:
            List[str]: track names
        """
        return list(map(lambda t: t.name, self.tracks))

    class TrackIterator:
        """Iterated through dataset's tracks."""

        def __init__(self, tracks):
            self.tracks = tracks

        def __iter__(self):
            self.index = 0
            return self

        def __next__(self):
            if self.index >= len(self.tracks):
                raise StopIteration
            t = self.tracks[self.index]
            self.index += 1
            return t

    def trackIterator(self) -> "Dataset.TrackIterator":
        """The Track iterator of this dataset

        Returns:
            Dataset.TrackIterator: Use this to iterate over this datasets tracks.
        """
        return self.TrackIterator(self.tracks)

    def getFullDataset(self):
        """Connects to LOGS web API to retrive the full dataset and extends the current object.

        Raises:
            Exception: Server cannot be reached.
        """
        if not self.getUrl or not self.url:
            return

        # print(">>", self.formatValues)
        # print(urlparse(self.url))
        # print("url", self.url)
        result, error = self.getUrl(self.url, params={"formatValues": self.formatValues})
        # print(">>", json.dumps(result, indent=2, sort_keys=False))

        if error:
            raise Exception("Could not connect to '%s': %s" % (result.url, error))
        self.init(result)

    def __str__(self):
        # print(">>", self.__dict__)

        # for k, v in self.__dict__.items():
        #     if v == None:
        #         continue
        #     print(k, "->", v)

        return "Dataset: " + str(self.id)

    def __len__(self):
        return len(self.tracks)
