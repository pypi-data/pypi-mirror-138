from LOGSAPI.Dataset import Dataset
from typing import Callable, List, Tuple

class DatasetPage:
    """Represents a LOGS web API response dataset page from the dataset endpoint"""

    def __init__(
        self, response: Tuple[dict, str], getUrl: Callable[[str], Tuple[str, str]] = None, formatValues: bool = True
    ):
        """Creates a object from the API response.

        Args:
            response ([type]): The API response.
            getUrl (Callable, optional): A function to retrive further dataset pages. Defaults to None.

        Raises:
            Exception: [description]
        """
        result, error = response
        if error:
            raise Exception("Could not connect to '%s': %s" % (result.url, error))

        self.page = result["page"]
        self.pageSize = result["pageSize"]
        self.hasNextPage = result["hasNextPage"]
        self.nextPage = result["nextPage"]
        self.formatValues = formatValues

        self.__datasets = result["result"]
        self.getUrl = getUrl

    def __len__(self):
        return len(self.__datasets)

    def get(self, i) -> Dataset:
        """Get a specific dataset from the result page

        Args:
            i ([type]): The index of the dataset on the result page.

        Returns:
            Dataset: The specified dataset object or None if dataset index is invalid.
        """
        if i < 0 or i >= len(self.__datasets):
            return None

        return Dataset(self.__datasets[i], self.getUrl, formatValues=self.formatValues)

    def getAll(self) -> List[Dataset]:
        """Return a list of all dataset object on this result page.

        Returns:
            List[Dataset]: List of datasets.
        """
        return list(
            map(lambda d: Dataset(d, getUrl=self.getUrl, formatValues=self.formatValues), self.__datasets, self.getUrl)
        )

    def __setToUndef(self):
        self.page = -1
        self.hasNextPage = False
        self.nextPage = None
        self.__datasets = None

    def getNextPage(self) -> "DatasetPage":
        """Connects to LOGS web API to retrive the next dataset page for the same request.

        Returns:
            DatasetPage: The next dataset page or None if the current page is the last (or getUrl is undefined)
        """
        if not self.hasNextPage:
            return None

        if self.getUrl:
            response = self.getUrl(self.nextPage)
            return DatasetPage(response, self.getUrl, formatValues=self.formatValues)
        else:
            return None

    class DatasetPageIterator:
        """Iterates through the dataset pages of the current dataset request."""

        def __init__(self, currentPage):
            self.page = currentPage

        def __iter__(self):

            return self

        def __next__(self):
            p = self.page
            if p == None:
                raise StopIteration
            self.page = self.page.getNextPage()
            return p

    class DatasetIterator:
        """Iterates through the datasets of the current dataset request."""

        def __init__(self, currentPage):
            self.page = currentPage
            self.index = 0

        def __iter__(self):

            return self

        def __next__(self) -> Dataset:

            d = self.page.get(self.index)
            if d == None:
                self.page = self.page.getNextPage()
                if self.page == None:
                    raise StopIteration
                self.index = 0
                d = self.page.get(self.index)
                if d == None:
                    raise StopIteration

            self.index += 1
            return d

    def pageIterator(self) -> "DatasetPage.DatasetPageIterator":
        """The Page iterator of this request. Connect to the LOGS web API to retrive the next page of the request.

        Returns:
            Dataset.TrackIterator: Use this to iterate over the pages of the request.
        """

        return self.DatasetPageIterator(self)

    def datasetIterator(self) -> "DatasetPage.DatasetIterator":
        """The dataset iterator of this request. Iterates of all datasets on this page and connects automatically
        to the LOGS web API to retrive the next page of the request.

        Returns:
            Dataset.TrackIterator: Use this to iterate over all datasets of the request.
        """
        return self.DatasetIterator(self)
        # return DatasetIterator(lambda a: a)
