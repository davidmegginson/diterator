""" Iterator through IATI activities from D-Portal """

import collections, datetime, io, requests, xml.dom.pulldom

from diterator.wrappers import Activity


API_ENDPOINT = "http://www.d-portal.org/q"


class Iterator:
    """ Parse XML activities from the D-Portal Q API """
    
    def __init__ (self, search_params={}, deduplicate=True):
        self.search_params = dict(search_params)
        self.activity_queue = collections.deque()
        self.deduplicate = deduplicate
        if deduplicate:
            self.identifiers_seen = set()

        if not "from" in self.search_params:
            self.search_params["from"] = "act,country,sector"

        # Ignore and override anything the user supplied for these
        self.search_params["limit"] = 100
        self.search_params["offset"] = 0
        self.search_params["form"] = "xml"
        
    def __iter__ (self):
        return self

    def __next__ (self):
        if len(self.activity_queue) > 0:
            activity = Activity(self.activity_queue.popleft())
            if self.deduplicate:
                if activity.identifier in self.identifiers_seen:
                    # recurse
                    return self.__next__()
                else:
                    self.identifiers_seen.add(activity.identifier)
            return activity
        else:
            result = requests.get(API_ENDPOINT, params=self.search_params)
            self.search_params["offset"] += self.search_params["limit"]
            result.raise_for_status() # raise an exception for an HTTP error status
            
            dom = xml.dom.pulldom.parseString(result.text)
            for event, node in dom:

                # parse all of the iati-activity nodes in the result page
                if event == xml.dom.pulldom.START_ELEMENT and node.tagName == "iati-activity":
                    dom.expandNode(node)
                    self.activity_queue.append(node)

            if len(self.activity_queue) == 0:
                # Didn't find any new activities
                raise StopIteration()
            else:
                # Recurse -- the queue will be populated now
                return self.__next__()


class XMLIterator:
    """ Iterate through XML activities from an IATI activity document, via a stream, URL, or filename. """

    def __init__ (self, filename_or_stream=None, url=None):
        if filename_or_stream:
            self.parser = xml.dom.pulldom.parse(filename_or_stream)
        elif url:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            self.parser = xml.dom.pulldom.parse(ResponseStream(response.iter_content(64)))

    def __iter__ (self):
        return self

    def __next__ (self):
        for event, node in self.parser:
                # parse all of the iati-activity nodes in the result page
                if event == xml.dom.pulldom.START_ELEMENT and node.tagName == "iati-activity":
                    self.parser.expandNode(node)
                    return Activity(node)

        raise StopIteration()
        
        
class ResponseStream(object):
    """ The otherwise-great requests library makes it stupidly hard to get a file-like object for a response.
    This wrapper comes from https://gist.github.com/obskyr/b9d4b4223e7eaf4eedcd9defabb34f13

    """
    def __init__(self, request_iterator):
        self._bytes = io.BytesIO()
        self._iterator = request_iterator

    def _load_all(self):
        self._bytes.seek(0, io.SEEK_END)
        for chunk in self._iterator:
            self._bytes.write(chunk)

    def _load_until(self, goal_position):
        current_position = self._bytes.seek(0, io.SEEK_END)
        while current_position < goal_position:
            try:
                current_position += self._bytes.write(next(self._iterator))
            except StopIteration:
                break

    def tell(self):
        return self._bytes.tell()

    def read(self, size=None):
        left_off_at = self._bytes.tell()
        if size is None:
            self._load_all()
        else:
            goal_position = left_off_at + size
            self._load_until(goal_position)

        self._bytes.seek(left_off_at)
        return self._bytes.read(size)
    
    def seek(self, position, whence=io.SEEK_SET):
        if whence == io.SEEK_END:
            self._load_all()
        else:
            self._bytes.seek(position, whence)

