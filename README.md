Iterator through IATI activities from D-Portal
==============================================

This library makes it easy to download IATI activities from D-Portal and iterate through them. It takes care of issues like paging, XML parsing, etc. There are wrapper classes for the most-common properties of an IATI activity, and the entire XML is available through XPath queries (if desired).

## Examples

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

Though normally, to iterate through transactions, you'd just do something like

```
for transaction in activity.transactions:
    print(transaction.type, transaction.date, transaction.currency, transaction.value)
```

There are also helper functions to group sectors, participating organisations, etc

```
for sector in activity.sectors_by_vocabulary.get("10", []):
    print(sector.code, sector.percentage, sector.name)
```


## Author

David Megginson


## License

This code is released into the Public Domain and comes with no warranty of any kind. Use at your own risk.
