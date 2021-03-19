""" Simple demo code """

from . import Iterator

activities = Iterator({
    "country_code": "so",
    "day_gteq": "2020-01-01",
    "limit": 5,
})
for i, activity in enumerate(activities):
    print(activity.default_language, activity.identifier, activity.title)
    for transaction in activity.transactions:
        print("\t", transaction.type, transaction.currency, transaction.value)
    if i > 5:
        break
