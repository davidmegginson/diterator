Iterator through IATI activities from D-Portal
==============================================

This library makes it easy to download [IATI](https://iatistandard.org) activities from [D-Portal](https://d-portal.org) and iterate through them. It takes care of issues like paging, XML parsing, etc. There are wrapper classes for the most-common properties of an [IATI activity](https://iatistandard.org/en/iati-standard/203/activity-standard/), and the entire XML is available through [XPath](https://en.wikipedia.org/wiki/XPath) queries (if desired).

## Usage

The _diterator.iterator.Iterator_ class (also available from the package root) creates a stream of IATI activities from D-Portal matching the query parameters you provide:

```
from diterator import Iterator

activities = Iterator({
    "country_code": "ye",
})

for activity in activities:
    print("Activity", activity.identifier)
```

By default, the Iterator class filters duplicate activities out of the results. If you don't want that behaviour, add the parameter ``deduplicate=False``

Each activity appears inside a wrapper that gives you easy access to the most-common properties (see documentation below). You can also use [XPath](https://en.wikipedia.org/wiki/XPath) queries to pull out specific pieces of information.

### D-Portal query parameters

Full documentation of the D-Portal query parameters is available here:

https://github.com/devinit/D-Portal/blob/master/documents/dstore_q.md

The most common D-Portal query parameters include the following:

Parameter | Description | Example
-- | -- | --
reporting | The reporting org name | World Health Organization
reporting_code | The reporting org IATI code | XM-DAC-928
aid | IATI identifier for a specific activity | XM-DAC-928-ER-2016-17-02.006.AF01.ERI01
sector_code | A specific OECD-DAC sector code | 72050
title | The activity title in English. | Technical assistance to enable (...)
description | The activity description in English. | This activity will (...)
country_code | The [ISO 3166:1-alpha2 code](https://iatistandard.org/en/iati-standard/203/codelists/country/) for a recipient country. | SO
location_name | A name of a specific location (as specified by the publisher). | Tombali
day_start | The activity's start date | 2020-01-01
day_end | The activity's end date | 2020-12-31
status_code | The activity's [status code](https://iatistandard.org/en/iati-standard/203/codelists/activitystatus/) | 2

Use "|" to separate multiple values, and append "\_nteq" to the property name for "not equal", "\_gt" for "greater than", "\_gteq" for "greater than or equal", "\_lt" for "less than", "\_lteq" for less than or equal, "\_glob" for case-sensitive string matching with "*" and "\_" as wildcards, or "\_like" for case-insensitive string matching.

For example, if you wanted to find all activities for Somalia or Kenya in 2020, you could pass this query to the iterator:

```
from diterator import Iterator

activities = Iterator({
    "country_code": "SO|KE",
    "day_end_gteq": "2020-01-01",
    "day_start_lteq": "2020-12-31",
})
```

If you wanted to further filter to only activities with a DAC sector code starting with "7", you could use

```
activities = Iterator({
    "country_code": "SO|KE",
    "day_end_gteq": "2020-01-01",
    "day_start_lteq": "2020-12-31",
    "sector_code_glob": "7????",
})
```

Again, go to the [D-Portal Q API documentation](https://github.com/devinit/D-Portal/blob/master/documents/dstore_q.md) for full details.

### Using an XML file or URL instead of the D-Portal Q API

If you prefer to read IATI activities directly from a URL (e.g. one found at the [IATI Registry](https://iatiregistry.org/)) or a local file, then you can use the XMLIterator class instead:

```
from diterator import XMLIterator

activities = XMLIterator(url="https://static.rijksoverheid.nl/bz/IATIACTIVITIES20202021.xml")
for activity in activities:
    print(activity.identifier)
```

If your source is a URL rather than a file object or local file name, as in the example above, then you need to put "url=" before it. For a local XML file, leave the "url=" out, so the above example would look like this:

```
from diterator import XMLIterator

activities = diterator.XMLIterator("IATIACTIVITIES20202021.xml")
for activity in activities:
    print(activity.identifier)
```

## Wrapper objects

Each activity will be returned wrapped in the Python class diterator.wrappers.Activity, which provides simple access to many of the common properties. All wrappers support some common properties for direct queries against the XML (in case the information you need isn't covered by the properties):

Method | Description | Example
-- | -- | --
get_text(xpath_expr) | Get the text content of the _first_ [DOM](https://docs.python.org/3/library/xml.dom.html) node matching the [XPath](https://en.wikipedia.org/wiki/XPath) expression. | activity.get_text("reporting-org/@ref")
get_narrative(xpath_expr) | Get the multilingual narrative content inside the first node matching the XPath expression. |  activity.get_narrative("title")
get_organisation(xpath_expr) | Get the organisation info for the first node matching the XPath expression. | transaction.get_organisation("provider-org")
get_node(xpath_expr) | Get the first first DOM node matching the XPath expression. | transaction.get_node("value")
get_nodes(xpath_expr) | Get a list of _all_ the DOM nodes matching the XPath expression. | activity.get_nodes("sector[@vocabulary=10]")
extract_node_text(node) | Extract the text from an element or attribute DOM node.

### Activity object

This represents the top level of an IATI activity. Available properties:

Property | Description | Return value
-- | -- | --
default_currency | The activity's default ISO 4217 currency code. | string
default_language | The default ISO 639 language code for text content in the activity. | string
humanitarian | "Is humanitarian" flag at the activity level. | boolean
identifier | The unique IATI identifier for the activity. | String
reporting_org | The reporting organisation. | Organisation object
secondary_reporter | If true, the reporting org is not involved in the activity. | boolean
title | The activity title, possibly in multiple languages. | NarrativeText
description | The activity description, possibly in multiple languages. | NarrativeText
participating_orgs | All participating organisations. | list of Organisation
participating_orgs_by_role | Participating organisations grouped by [role code](https://iatistandard.org/en/iati-standard/203/codelists/organisationrole/). | dict with lists of Organisation
participating_orgs_by_type | Participating organisations grouped by [type code](https://iatistandard.org/en/iati-standard/203/codelists/organisationrole/). | dict with lists of Organisation
other_identifiers | List of non-IATI alternative activity identifiers | list of Identifier
activity_status | A code describing the [status of the activity](https://iatistandard.org/en/iati-standard/203/codelists/activitystatus/). | string
is_active | Convenience method to show if the activity is currently active. | boolean
activity_dates | Activity dates grouped by the [date-type code](https://iatistandard.org/en/iati-standard/203/codelists/activitydatetype/). | dict with strings
start_date_planned | The planned start date in ISO 8601 format, if specified. | string
start_date_actual | The actual start date in ISO 8601 format, if specified. | string
end_date_planned | The planned end date in ISO 8601 format, if specified. | string
end_date_actual | The actual end date in ISO 8601 format, if specified. | string
contact_info | _Not yet implemented_ |
activity_scope | A [geographical-scope code](https://iatistandard.org/en/iati-standard/203/codelists/activityscope/) for the activity, if available. | string
recipient_countries | A list of recipient countries. | list of CodedItem
recipient_regions | A list of recipient regions. | list of CodedItem
locations | A list of specific project locations. | list of Location
locations_by_class | Specific project locations, grouped by [class code](https://iatistandard.org/en/iati-standard/203/codelists/geographiclocationclass/). | dict with lists of Location
sectors | A list of project sectors (all vocabularies). | list of CodedItem
sectors_by_vocabulary | Sectors grouped by [sector vocabulary code](https://iatistandard.org/en/iati-standard/203/codelists/sectorvocabulary/). | dict with lists of CodedItem
tags | Activity tags (all vocabularies). | list of CodedItem
tags_by_vocabulary | Activity tags grouped by [tag vocabulary code](https://iatistandard.org/en/iati-standard/203/codelists/tagvocabulary/). | dict with lists of CodedItem
humanitarian_scopes | Humanitarian scopes (all types and vocabularies). | list of CodedItem
humanitarian_scopes_by_type | Humanitarian scopes grouped by [type code](https://iatistandard.org/en/iati-standard/203/codelists/humanitarianscopetype/). | dict with lists of CodedItem
humanitarian_scopes_by_vocabulary | Humanitarian scopes grouped by [vocabulary code](https://iatistandard.org/en/iati-standard/203/codelists/humanitarianscopevocabulary/). | dict with lists of CodedItem
policy_marker | _Not yet implemented_ | 
collaboration_type | Code for the [collaboration type](https://iatistandard.org/en/iati-standard/203/codelists/collaborationtype/), if specified. | string
default_flow_type | Code for the default [flow type](https://iatistandard.org/en/iati-standard/203/codelists/flowtype/), if specified. | string
default_finance_type | Code for the default [finance type](https://iatistandard.org/en/iati-standard/203/codelists/financetype/), if specified. | string
default_aid_types | List of default [aid type codes](https://iatistandard.org/en/iati-standard/203/codelists/aidtype/) | list of CodedItem
default_aid_types_by_vocabulary | Default aid types grouped by [vocabulary code](https://iatistandard.org/en/iati-standard/203/codelists/aidtypevocabulary/) | dict with CodedItem
default_tied_status | Code for the default [tied status](https://iatistandard.org/en/iati-standard/203/codelists/tiedstatus/) | string
budget | _Not yet implemented_ | 
planned_disbursement | _Not yet implemented_ | 
capital_spend | _Not yet implemented_ | 
transactions | All transactions associated with the activity. | list of Transaction objects
transactions_by_type | Transactions grouped by their [type code](https://iatistandard.org/en/iati-standard/203/codelists/transactiontype/). | dict with Transaction
document_link | _Not yet implemented_ | 
related_activity | _Not yet implemented_ | 
legacy_data | _Not yet implemented_ | 
conditions | _Not yet implemented_ | 
result | _Not yet implemented_ | 
crs_add | _Not yet implemented_ | 
fss | _Not yet implemented_ | 

### Transaction object

Represents a transaction inside an IATI activity. 

The class will return default values from the activity if they are not specified for the transaction. If you want to see if the transaction actually specifies the properties itself, use the get_node or get_text methods. For example, the following will specify whether the _humanitarian_ attribute, sectors, and aid type actually appear on the transaction itself:

```
transaction_humanitarian_flag = transaction.get_text("@humanitarian")
tranaction_has_own_sectors = (len(transaction.get_nodes("sector")) > 0)
transaction_has_own_aid_type = (transaction.get_node("aid-type") is not None)
```

Property | Description | Return value
-- | -- | --
activity | The parent activity. | Activity
ref | The transaction reference, if available. | string
humanitarian | "Is humanitarian" flag at the transaction level (overrides activity default). If the transaction has no flag, return the activity's value as a default. | boolean
date | Transaction date in ISO 8601 format. | string
type | Type code for the transaction. | string
value | Transaction value in its currency (may be negative). | float
currency | ISO 4217 currency code for the transaction (overrides activity default). | string
value_date | Date to use for currency conversion, in ISO 8601 format. | string
description | Descriptive text for the transaction, possibly in multiple languages. | NarrativeText
provider_org | The source of the funds in the transaction. | Organisation
receiver_org | The destination of the funds in the transaction. | Organisation
disbursement_channel | A code for the transaction's [disbursment channel](https://iatistandard.org/en/iati-standard/203/codelists/disbursementchannel/). | string
sectors | A list of transaction sectors (all vocabularies), overriding the activity defaults. If the transaction has no sectors, return the activity's sectors as a default. | list of CodedItem
sectors_by_vocabulary | Transaction sectors grouped by [sector vocabulary code](https://iatistandard.org/en/iati-standard/203/codelists/sectorvocabulary/). Will default to the activity's sectors if the transaction does not specify its own. | dict with lists of CodedItem
recipient_countries | A list of recipient countries, overriding the activity defaults. If the transaction has no recipient countries, return the activity's recipient countries as a default. | list of CodedItem
recipient_regions | A list of recipient regions, overriding the activity defaults. If the transaction has no recipient regions, return the activity's recipient regions as a default. | list of CodedItem
flow_type | A code for the transaction's [flow type](https://iatistandard.org/en/iati-standard/203/codelists/flowtype/). If the transaction has no flow type, return the activity's default flow type. | string
finance_type | A code for the transaction's [finance type](https://iatistandard.org/en/iati-standard/203/codelists/financetype/). If the transaction has no finance type, return the activity's default finance type. | string
aid_types | A list of [aid type codes](https://iatistandard.org/en/iati-standard/203/codelists/aidtype/) specified for the transaction. If the transaction has no aid types, return the activity's default aid types. | list of CodedItem
aid_types_by_vocabulary | A dict of [aid type codes](https://iatistandard.org/en/iati-standard/203/codelists/aidtype/) specified for the transaction, keyed by vocabulary. If the transaction has no aid types, return the activity's default aid types. | list of CodedItem
tied_status | A code for the transaction's [tied status](https://iatistandard.org/en/iati-standard/203/codelists/tiedstatus/). If the transaction has no tied status, return the activity's default tied status. | string

### NarrativeText object

Represents multilingual text wherever it is allowed in IATI. If the language of a translation is unspecified, it will default to the parent activity's default_language property. If you us this object in a string context, it will return the text in the activity's default language (if available) or the first translation specified, so if you wrap this in str(), use it in a print() function, etc, you'll get a simple string.

Property | Description | Return value
-- | -- | --
activity | The parent activity. | Activity
narratives | All available translations, keyed by language. | dict of string

### Organisation object

Represents an organisation (in any context) inside an IATI activity. Some properties will always return None, depending on context.

Property | Description | Return value
-- | -- | --
activity | The parent activity. | Activity
ref | The organisation identifier, if available. | string
type | The organisation's type code. | string
role | The organisation's role code (if relevant). | string
activity_id | The organisation's own IATI identifier for the activity (if relevant). | string
name | All translations of the organisation's name. | NarrativeText

### Location object

Wrapper for a specific location associated with an activity.

Property | Description | Return value
-- | -- | --
activity | The parent activity. | Activity
ref | The location's code, if available. | string
location_reach | The location's reach code, if available. | string
location_ids | Identifiers provided for the location, all vocabularies. | list of CodedItem
name | All translations of the location's name. | NarrativeText
description | All translations of the location's description. | NarrativeText
activity_description | Translations of the description of the activity as it applies in this location. | NarrativeText
administratives | Administrative codes for this location. | list of CodedItem
point | Latitude and longitude, space separated. | string
point_reference_system | Name of the lat/lon reference system used. | string
exactness | Code for the location exactness. | string
location_class | Code for the location class. | string
feature_designation | Code for the location's feature designation. | string

### CodedItem object

This class applies to any item that can have a code and optionally, a vocabulary and/or descriptive text. In a string context (e.g. print() or str()), this object will return its code property. Some properties will always return None, depending on context.

Property | Description | Return value
-- | -- | --
activity | The parent activity. | Activity
code | Code for this item. | string
vocabulary | Code for the (relevant) vocabulary in use. | string
narrative | Multiple translations of this item's descriptive text. | NarrativeText
percentage | The percentage applicable to this item within its context and vocabulary, if relevant. | string
type | Code for the type of the item, if relevant. | string
level | code for the level of the item, if relevant. | string

### Identifier object

Represents a non-IATI identifier (e.g. iati-activity/other-identifier).

Property | Description | Return value
-- | -- | --
activity | The parent activity. | Activity
ref | The alternative identifier. | string
type | The identifier [type code](https://iatistandard.org/en/iati-standard/203/codelists/otheridentifiertype/). | string
owner_org | The organisation that owns the identifier, if specified. | Organisation

## Example

```
# Print the identifier and title of every activity for Somalia from 2019 to 2021

from diterator import Iterator

activities = Iterator({
    "country_code": "so",
    "day_end_gteq": "2019-01-01",
    "day_start_lteq": "2021-12-31",
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

There are also helper properties to group sectors, participating organisations, etc

```
for sector in activity.sectors_by_vocabulary.get("10", []):
    print(sector.code, sector.percentage, sector.name)
```

## Author

David Megginson


## License

This code is released into the Public Domain and comes with no warranty of any kind. Use at your own risk.
