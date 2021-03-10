""" Iterator through IATI activities from D-Portal """

import collections, datetime, requests, xml.dom.pulldom

from diterator.wrappers import Activity


API_ENDPOINT = "http://www.d-portal.org/q"

class Iterator:

    def __init__ (self, search_params={}):
        self.search_params = dict(search_params)
        self.activity_queue = collections.deque()

        # a little help with dates
        if "year_min" in self.search_params:
            self.search_params["day_end_lteq"] = (datetime.datetime(self.search_params["year_min"], 12, 31) - datetime.datetime(1970, 1, 1)).days
            self.search_params.pop("year_min")
        if "year_max" in self.search_params:
            self.search_params["day_start_gteq"] = (datetime.datetime(self.search_params["year_max"], 1, 1) - datetime.datetime(1970, 1, 1)).days
            self.search_params.pop("year_min")

        # we need to have select tables (if not supplied)
        if "from" not in self.search_params:
            self.search_params["from"] = "act,country,sector"

        self.search_params["limit"] = 25
        self.search_params["offset"] = 0
        self.search_params["form"] = "xml"
        
    def __iter__ (self):
        return self

    def __next__ (self):
        if len(self.activity_queue) > 0:
            return Activity(self.activity_queue.popleft())
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
        
        
if __name__ == "__main__":
    activities = Iterator({
        "country_code": "so",
        "year_min": 2020,
    })
    for activity in activities:
        print(activity.identifier)
