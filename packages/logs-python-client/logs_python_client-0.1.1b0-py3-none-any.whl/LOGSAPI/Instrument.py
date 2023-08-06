from typing import Callable, Tuple


class Instrument:
    """Represents a LOGS dataset instrument."""

    def __init__(self, data: dict, getUrl: Callable[[str], Tuple[str, str]] = None):
        """Create a instrument from a dictionary and retrives the full track from the LOGS web API

        Args:
            data (dict): Dictionary representing the track (e.g. from a LOGS web API response)
            getUrl (Callable, optional): A function to retrive full track data. Defaults to None.
        """
        self.getUrl = getUrl

        if data == None:
            data = {}

        self.__init(data)

    def __init(self, data: dict):
        self.id = data["id"] if "id" in data else None
        self.name = data["name"] if "name" in data else None

    def __str__(self):
        if not self.name:
            return "Instrument " + str(self.id)
        return self.name
