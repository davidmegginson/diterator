""" Wrapper classes for IATI DOM nodes """

import abc, xpath


class Base(abc.ABC):
    """ Abstract base class for all IATI wrappers """

    def __init__ (self, node, activity=None):
        self.node = node
        if activity is None:
            activity = self
        self.activity = activity

    def get_text (self, xpath_expr):
        """ Get the text associated with an XPath expression """
        return self.extract_node_text(self.get_node(xpath_expr))

    def get_narrative (self, xpath_expr):
        """ Get a NarrativeText object associated with an XPath expression """
        node = self.get_node(xpath_expr)
        if node:
            return NarrativeText(node, self.activity)
        else:
            return None

    def get_organisation (self, xpath_expr):
        """ Get an organisation object associated with an XPath expression """
        node = self.get_node(xpath_expr)
        if node:
            return Organisation(node, self.activity)
        else:
            return None

    def get_node (self, xpath_expr, base_node=None):
        """ Return the first matching node for an XPath expression """
        nodes = self.get_nodes(xpath_expr, base_node)
        if len(nodes) == 0:
            return None
        else:
            return nodes[0]

    def get_nodes (self, xpath_expr, base_node=None):
        """ Return all matching nodes for an XPath expression """
        if base_node is None:
            base_node = self.node
        return xpath.find(xpath_expr, base_node)

    def extract_node_text (self, node):
        """ Extract text from a DOM node """
        if not node:
            return None
        elif node.nodeType == node.ELEMENT_NODE:
            s = ""
            for child in node.childNodes:
                if child.nodeType == child.TEXT_NODE:
                    s += child.data
            return s
        elif node.nodeType == node.ATTRIBUTE_NODE:
            return node.value
        else:
            raise Exception("Cannot get text for node of type {}".format(node.nodeType))
        

class Activity(Base):
    """ Wrapper class for an iati-activity node """

    def __init__ (self, node):
        super().__init__(node)

    @property
    def default_currency (self):
        """ Return the default ISO 4217 currency code for the activity's transactions """
        return self.get_text("@default-currency").upper()

    @property
    def default_language (self):
        """ Return the default ISO 639-2 language code for the activity's text """
        return self.node.getAttribute("xml:lang").lower()

    @property
    def humanitarian (self):
        """ Return a truthy value (usually "1") if the activity as a whole is flagged as humanitarian """
        return self.get_text("@humanitarian")

    @property
    def identifier (self):
        """ Return the activity's IATI identifier """
        return self.get_text("iati-identifier")

    @property
    def reporting_org (self):
        """ Return an Organisation object for the reporting-org """
        return self.get_organisation("reporting-org")

    @property
    def secondary_reporter (self):
        """ Return a truthy value if the organisation is not directly responsible for the activity """
        return self.get_text("reporting-org/@secondary-reporter")

    @property
    def participating_orgs (self):
        """ Return a list of participating organisations """
        return [Organisation(node, self) for node in self.get_nodes("participating-org")]

    @property
    def title (self):
        """ Return a NarrativeText object with all language versions of the activity's title """
        return self.get_narrative("title")

    @property
    def description (self):
        """ Return a NarrativeText object with all language versions of the activity's description """
        return self.get_narrative("description")

    @property
    def transactions (self):
        """ Return a list of Transaction objects for the activity """
        return [Transaction(node, self) for node in self.get_nodes("transaction")]


class Transaction(Base):
    """ Wrapper class for a transaction node """

    def __init__ (self, node, activity):
        super().__init__(node, activity)

    @property
    def ref (self):
        """ Return the transaction's @ref attribute, or None """
        return self.get_text("@ref")

    @property
    def humanitarian (self):
        """ Return a truthy value (usually "1") if this specific transaction is flagged as humanitarian """
        return self.get_text("@humanitarian")

    @property
    def date (self):
        """ Return the transaction date in ISO 8601 format """
        return self.get_text("transaction-date/@iso-date")

    @property
    def type (self):
        """ Return a code for the transaction type from https://iatistandard.org/en/iati-standard/203/codelists/transactiontype/ """
        return self.get_text("transaction-type/@code")

    @property
    def value (self):
        """ Return the transaction value (may be negative) """
        return float(self.get_text("value"))

    @property
    def currency (self):
        """ Return an ISO 4217 code for the transaction's currency, or the activity's default currency if not specified """
        currency = self.get_text("value/@currency")
        if currency:
            return currency
        else:
            return self.activity.default_currency

    @property
    def value_date (self):
        """ Return a value date in ISO 8601 format to use for conversion to other currencies """
        return self.get_text("value/@value-date")

    @property
    def description (self):
        """ Return a NarrativeText object with translations of the transaction's description, or None """
        return self.get_narrative("description")

    @property
    def provider_org (self):
        """ Return an Organisation object for the provider of incoming funds """
        return self.get_organisation("provider-org")

    @property
    def provider_activity_id (self):
        """ Return the IATI activity id that's the source of incoming funds """
        return self.get_text("provider-org/@provider-activity-id")

    @property
    def receiver_org (self):
        """ Return an Organisation object for the provider of incoming funds """
        return self.get_organisation("provider-org")

    @property
    def receiver_activity_id (self):
        """ Return the IATI activity id that's the source of incoming funds """
        return self.get_text("provider-org/@provider-activity-id")


class NarrativeText(Base):
    """ Wrapper class for narrative text in multiple languages """

    def __init__ (self, node, activity):
        super().__init__(node, activity)

    @property
    def narratives (self):
        """ Return a dict of all translations, keyed by ISO 639-2 language code
        If not specified, use the activity's default language.

        """
        result = {}
        for node in self.get_nodes("narrative"):
            lang = node.getAttribute("xml:lang")
            if not lang:
                lang = self.activity.default_language
            result[lang] = self.extract_node_text(node)
        return result

    def __str__ (self):
        """ Extract a single default translation as a string.
        If there is a translation in the activity's default language, use that.
        Otherwise, if there is an English translation, use that.
        Otherwise, return the first translation provided.

        """
        narratives = self.narratives
        if self.activity.default_language in self.narratives:
            return self.narratives[self.activity.default_language]
        elif "en" in self.narratives:
            return self.narratives["en"]
        else:
            return self.narratives.values[0]


class Organisation(Base):
    """ Wrapper class for a node describing an organisation
    Includes only intrinsic properties for an org, not ones that vary by context

    """

    def __init__ (self, node, activity):
        super().__init__(node, activity)

    @property
    def ref (self):
        """ Return the organisation's identifier, or None """
        return self.node_text("@ref")

    @property
    def type (self):
        """ Return the organisation's type code from https://iatistandard.org/en/iati-standard/203/codelists/organisationtype/ """
        return self.node_text("@type")

    @property
    def name (self):
        """ Return a NarrativeText object with different translations of the org's name """
        return self.get_narrative(".")

    def __str__ (self):
        return str(self.name)

