""" Iterator through IATI activities from D-Portal """

import collections, datetime, requests, xml.dom.pulldom

from diterator.wrappers import Activity


API_ENDPOINT = "http://www.d-portal.org/q"

class Iterator:

    def __init__ (self, search_params={}, deduplicate=True):
        self.search_params = dict(search_params)
        self.activity_queue = collections.deque()
        self.deduplicate = deduplicate
        if deduplicate:
            self.identifiers_seen = set()

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
        
        
if __name__ == "__main__":
    activities = Iterator({
        "country_code": "so",
        "day_gteq": "2020-01-01",
    }, deduplicate=True)
    for i, activity in enumerate(activities):
        print(activity.default_language, activity.identifier, activity.title)
        for transaction in activity.transactions:
            print("\t", transaction.type, transaction.currency, transaction.value)
        if i > 5:
            break
