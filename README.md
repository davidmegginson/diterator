Iterator through IATI activities from D-Portal
==============================================

# Example

```
import diterator.iterator

activities = diterator.iterator.Iterator({
    "country_code": "so",
    "year_min": 2019,
    "year_max": 2021,
})

for activity in activities:
    print(activity.identifier, activity.title)
```

You can also get at anything in an activity via the DOM and XPath:

```
transaction_nodes = activity.get_nodes("transaction")

identifier = activity.get_text("iati-identifier")
```
