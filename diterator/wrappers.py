""" Wrapper classes for IATI DOM nodes """

import abc, xpath


class Base(abc.ABC):
    """ Abstract base class for all IATI wrappers """

    def __init__ (self, node, activity=None):
        self.node = node
        if activity is None:
            activity = self
        self.activity = activity

    def get_text (self, xpath_expr, base_node=None):
        """ Get the text associated with an XPath expression """
        return self.extract_node_text(self.get_node(xpath_expr, base_node))

    def get_narrative (self, xpath_expr, base_node=None):
        """ Get a NarrativeText object associated with an XPath expression """
        node = self.get_node(xpath_expr, base_node)
        if node:
            return NarrativeText(node, self.activity)
        else:
            return None

    def get_organisation (self, xpath_expr, base_node=None):
        """ Get an organisation object associated with an XPath expression """
        node = self.get_node(xpath_expr, base_node)
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
        return is_truthy(self.get_text("@humanitarian"))

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
        return is_truthy(self.get_text("reporting-org/@secondary-reporter"))

    @property
    def title (self):
        """ Return a NarrativeText object with all language versions of the activity's title """
        return self.get_narrative("title")

    @property
    def description (self):
        """ Return a NarrativeText object with all language versions of the activity's description """
        return self.get_narrative("description")

    @property
    def participating_orgs (self):
        """ Return a list of participating organisations """
        return [Organisation(node, self) for node in self.get_nodes("participating-org")]

    @property
    def participating_orgs_by_role (self):
        """ Return a dict of participating organisations, keyed by their role codes (as strings)
        See https://iatistandard.org/en/iati-standard/203/codelists/organisationrole/

        """
        role_map = {}
        for org in self.participating_orgs:
            role_map.setdefault(org.role, [])
            role_map[org.role].append(org)
        return role_map

    @property
    def participating_orgs_by_type (self):
        """ Return a dict of participating organisations, keyed by their role codes (as strings)
        See https://iatistandard.org/en/iati-standard/203/codelists/organisationrole/

        """
        type_map = {}
        for org in self.participating_orgs:
            type_map.setdefault(org.type, [])
            type_map[org.type].append(org)
        return type_map

    @property
    def other_identifiers (self):
        """ Return a list of Identifier objects for alternative, non-IATI activity identifiers """
        identifiers = []
        for node in self.get_nodes("other-identifier"):
            identifiers.append(Identifier(node, self))
        return identifiers

    @property
    def activity_status (self):
        """ Return a code for the activity status
        See https://iatistandard.org/en/iati-standard/203/codelists/activitystatus/

        """
        return self.get_text("activity-status/@code")

    @property
    def is_active (self):
        """ Convenience method: return True if the activity status is "2" (Implementation) """
        return (self.activity_status == "2")

    # activity-date

    @property
    def activity_dates (self):
        """ Return a dict of activity dates, keyed by the type code
        See https://iatistandard.org/en/iati-standard/203/codelists/activitydatetype/

        """
        date_map = {}
        for node in self.get_nodes("activity-date"):
            date_map[self.get_text("@type", node)] = self.get_text("@iso-date", node)
        return date_map

    @property
    def start_date_planned (self):
        """ Convenience method to return the planned start date (@type=1) """
        return self.get_text("activity-date[@type=1]/@iso-date")

    @property
    def start_date_actual (self):
        """ Convenience method to return the actual start date (@type=2) """
        return self.get_text("activity-date[@type=2]/@iso-date")

    @property
    def end_date_planned (self):
        """ Convenience method to return the planned end date (@type=3) """
        return self.get_text("activity-date[@type=3]/@iso-date")

    @property
    def end_date_actual (self):
        """ Convenience method to return the actual end date (@type=3) """
        return self.get_text("activity-date[@type=4]/@iso-date")

    # contact-info

    @property
    def activity_scope (self):
        """ Return the activity scope as a CodedItem, if present 
        See https://iatistandard.org/en/iati-standard/203/codelists/activityscope/

        """
        return self.get_text("activity-scope/@code")

    @property
    def recipient_countries (self):
        """ Return a list of recipient countries as CodedItem objects """
        return [CodedItem(node, self) for node in self.get_nodes("recipient-country")]
    
    @property
    def recipient_regions (self):
        """ Return a list of recipient regions as CodedItem objects """
        return [CodedItem(node, self) for node in self.get_nodes("recipient-region")]
    
    @property
    def locations (self):
        """ Return a list of Location objects """
        return [Location(node, self) for node in self.get_nodes("location")]

    @property
    def locations_by_class (self):
        """ Return a map of locations keyed by location class
        See https://iatistandard.org/en/iati-standard/203/codelists/geographiclocationclass/

        """
        class_map = {}
        for location in self.locations:
            class_map.setdefault(location.location_class, [])
            class_map[location.location_class].append(location)
        return class_map

    @property
    def sectors (self):
        """ Return a list of sectors as CodedItem objects """
        return [CodedItem(node, self) for node in self.get_nodes("sector")]

    @property
    def sectors_by_vocabulary (self):
        """ Return a map of sectors, keyed by @vocabulary 
        See https://iatistandard.org/en/iati-standard/203/codelists/sectorvocabulary/

        """
        sector_map = {}
        for sector in self.sectors:
            sector_map.setdefault(sector.vocabulary, [])
            sector_map[sector.vocabulary].append(sector)
        return sector_map

    @property
    def tags (self):
        """ Return a list of tags as CodedItem objects """
        return [CodedItem(node, self) for node in self.get_nodes("tag")]

    @property
    def tags_by_vocabulary (self):
        """ Return a map of tags, keyed by @vocabulary
        See https://iatistandard.org/en/iati-standard/203/codelists/tagvocabulary/

        """
        tag_map = {}
        for tag in self.tags:
            tag_map.setdefault(tag.vocabulary, [])
            tag_map[tag.vocabulary].append(tag)
        return tag_map

    # country-budget-items

    @property
    def humanitarian_scopes (self):
        return [CodedItem(node, self) for node in self.get_nodes("humanitarian-scope")]

    @property
    def humanitarian_scopes_by_type (self):
        """ See https://iatistandard.org/en/iati-standard/203/codelists/humanitarianscopetype/ """
        type_map = {}
        for scope in self.humanitarian_scopes:
            type_map.setdefault(scope.type, [])
            type_map[scope.type].append(scope)
        return type_map

    @property
    def humanitarian_scopes_by_vocabulary (self):
        vocabulary_map = {}
        for scope in self.humanitarian_scopes:
            vocabulary_map.setdefault(scope.vocabulary, [])
            vocabulary_map[scope.vocabulary].append(scope)
        return vocabulary_map

    # policy-marker

    @property
    def collaboration_type (self):
        """ Return a code for the collaboration type, if present.
        See https://iatistandard.org/en/iati-standard/203/codelists/CollaborationType/

        """
        return self.get_text("collaboration-type/@code")

    @property
    def default_flow_type (self):
        """ Return a code for the default flow type, if present.
        See https://iatistandard.org/en/iati-standard/203/codelists/flowtype/

        """
        return self.get_text("default-flow-type/@code")

    @property
    def default_finance_type (self):
        """ Return a code for the default finance type, if present.
        See https://iatistandard.org/en/iati-standard/203/codelists/financetype/

        """
        return self.get_text("default-flow-type/@code")

    @property
    def default_aid_types (self):
        """ Return a list of CodedItems for default aid types.
        See https://iatistandard.org/en/iati-standard/203/codelists/aidtype/

        """
        items = []
        for node in self.get_nodes("default-aid-type"):
            items.append(CodedItem(node, self))
        return items

    @property
    def default_aid_types_by_vocabulary (self):
        """ Return a dict of CodedItems for default aid types, keyed by vocabulary.
        See https://iatistandard.org/en/iati-standard/203/codelists/aidtypevocabulary/

        """
        vocab_map = {}
        for type in self.default_aid_types:
            vocab_map.setdefault(type.vocabulary, [])
            vocab_map[type.vocabulary] = type
        return vocab_map

    @property
    def default_tied_status (self):
        """ Return a code for the default tied status, if present.
        See https://iatistandard.org/en/iati-standard/203/codelists/tiedstatus/

        """
        return self.get_text("default-tied-status/@code")

    # budget

    # planned-disbursement

    # capital-spend

    @property
    def transactions (self):
        """ Return a list of Transaction objects for the activity """
        return [Transaction(node, self) for node in self.get_nodes("transaction")]

    @property
    def transactions_by_type (self):
        """ Return a dict of transactions grouped by type code.
        See https://iatistandard.org/en/iati-standard/203/codelists/transactiontype/

        """
        type_map = {}
        for transaction in self.transactions:
            type_map.setdefault(transaction.type, [])
            type_map[transaction.type].append(transaction)
        return type_map

    # document-link

    # related-activity

    # legacy-data

    # conditions

    # result

    # crs-add

    # fss


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
        """ Return a truthy value (usually "1") if this specific transaction is flagged as humanitarian
        If there's no attribute, default to the activity value.
        If you want to see if the transaction actually has an attribute, use transaction.get_text("@humanitarian") instead.

        """
        s = self.get_text("@humanitarian")
        if s is not None:
            return is_truthy(s)
        else:
            return self.activity.humanitarian

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
    def receiver_org (self):
        """ Return an Organisation object for the provider of incoming funds """
        return self.get_organisation("receiver-org")

    @property
    def disbursement_channel (self):
        """ Return a code for the transaction's disbursement channel.
        See https://iatistandard.org/en/iati-standard/203/codelists/disbursementchannel/

        """
        return self.get_text("disbursement_channel/@code")

    @property
    def sectors (self):
        """ Return a list of sectors as CodedItem objects
        If no sectors are specified, return the activity's sectors instead.
        If you need to know if the transaction has its own sectors, use
        transaction.get_nodes("sector") to check.

        """
        nodes = self.get_nodes("sector")
        if len(nodes) > 0:
            return [CodedItem(node, self.activity) for node in nodes]
        else:
            return self.activity.sectors

    @property
    def sectors_by_vocabulary (self):
        """ Return a map of sectors, keyed by @vocabulary 
        Will return the activity's sectors if the transaction has none of its own.
        See https://iatistandard.org/en/iati-standard/203/codelists/sectorvocabulary/

        """
        sector_map = {}
        for sector in self.sectors:
            sector_map.setdefault(sector.vocabulary, [])
            sector_map[sector.vocabulary].append(sector)
        return sector_map

    @property
    def recipient_countries (self):
        """ Return a list of recipient countries as CodedItem objects
        Will return the activity's recipient countries if the transaction has none of its own.
        If you need to know if the transaction has its own, use transaction.get_nodes("recipient-country") to check.

        """
        nodes = self.get_nodes("recipient-country")
        if len(nodes) > 0:
            return [CodedItem(node, self.activity) for node in nodes]
        else:
            return self.activity.recipient_countries
    
    @property
    def recipient_regions (self):
        """ Return a list of recipient regions as CodedItem objects 
        Will return the activity's recipient regions if the transaction has none of its own.
        If you need to know if the transaction has its own, use transaction.get_nodes("recipient-region") to check.

        """
        nodes = self.get_nodes("recipient-region")
        if len(nodes) > 0:
            return [CodedItem(node, self.activity) for node in nodes]
        else:
            return self.activity.recipient_regions

    @property
    def flow_type (self):
        """ Return the transaction's flow type code as a string.
        Will return the activity's default flow type if there's no flow type on the transaction.
        See https://iatistandard.org/en/iati-standard/203/codelists/flowtype/

        """
        code = self.get_text("flow-type/@code")
        if code:
            return code
        else:
            return self.activity.default_flow_type
    
    @property
    def finance_type (self):
        """ Return the transaction's flow type code as a string.
        Will return the activity's default finance type if there's no flow type on the transaction.
        See https://iatistandard.org/en/iati-standard/203/codelists/financetype/

        """
        code = self.get_text("finance-type/@code")
        if code:
            return code
        else:
            return self.activity.default_finance_type

    @property
    def aid_types (self):
        """ Return the a list of CodedItems for the transaction's aid types.
        Will return the activity's default aid types if there's no aid type on the transaction.
        See https://iatistandard.org/en/iati-standard/203/codelists/aidtype/

        """
        nodes = self.get_nodes("aid-type")
        if nodes:
            return [CodedItem(node) for node in nodes]
        else:
            return self.activity.default_aid_types

    @property
    def aid_types_by_vocabulary (self):
        """ Return a dict of CodedItems for aid types, keyed by vocabulary.
        Will return the activity's default aid types if there's no aid type on the transaction.
        See https://iatistandard.org/en/iati-standard/203/codelists/aidtype/

        """
        vocab_map = {}
        for type in self.aid_types:
            vocab_map.setdefault(type.vocabulary, [])
            vocab_map[type.vocabulary] = type
        return vocab_map

    @property
    def tied_status (self):
        """ Return a code for the transaction's tied status.
	Will return the activity's default tied status if there's no tied status on the transaction.
        See https://iatistandard.org/en/iati-standard/203/codelists/tiedstatus/

        """
        code = self.get_text("tied-status/@code")
        if code:
            return code
        else:
            return self.activity.default_tied_status

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
        elif len(self.narratives) > 0:
            return list(self.narratives.values())[0]
        else:
            return ""


class Organisation(Base):
    """ Wrapper class for a node describing an organisation
    Includes only intrinsic properties for an org, not ones that vary by context

    This class knowingly violates data-modelling best practices by
    including the role and activity_id properties, both of which are
    part of the context in which an organisation is mentioned, rather
    than an intrinsic trait of the organisation itself. Otherwise, the
    interface would be unnecessarily complicated simply for the sake
    of being correct.

    """

    def __init__ (self, node, activity):
        super().__init__(node, activity)

    @property
    def ref (self):
        """ Return the organisation's identifier, or None """
        return self.get_text("@ref")

    @property
    def type (self):
        """ Return the organisation's type code
        See https://iatistandard.org/en/iati-standard/203/codelists/organisationtype/

        """
        return self.get_text("@type")

    @property
    def role (self):
        """ Return the organisation's @role code, if defined.
        See https://iatistandard.org/en/iati-standard/203/codelists/organisationrole/

        """
        return self.get_text("@role")

    @property
    def activity_id (self):
        """ Return the organisation's own IATI activity ID, if defined
        Will try @activity-id, @provider-activity-id, and @receiver-activity-id, in that order

        """
        id = self.get_text("@activity-id") # participating-org
        if not id:
            id = self.get_text("@provider-activity-id") # transaction/provider-org
        if not id:
            id = self.get_text("@receiver-activity-id") # transaction/receiver-org
        return id

    @property
    def name (self):
        """ Return a NarrativeText object with different translations of the org's name """
        return self.get_narrative(".")

    def __str__ (self):
        return str(self.name if self.name is not None else "")


class Location (Base):
    """ Wrapper for a location """

    def __init__ (self, node, activity):
        super().__init__(node, activity)

    @property
    def ref (self):
        return self.get_text("@ref")

    @property
    def location_reach (self):
        return self.get_node("location-reach/@code")

    @property
    def location_ids (self):
        return [CodedItem(node) for node in self.get_nodes("location-id")]

    @property
    def name (self):
        return self.get_narrative("name")

    @property
    def description (self):
        return self.get_narrative("description")

    @property
    def activity_description (self):
        return self.get_narrative("activity-description")

    @property
    def administratives (self):
        return [CodedItem(node) for node in self.get_nodes("administrative")]

    @property
    def point (self):
        return self.get_text("point/pos")

    @property
    def point_reference_system (self):
        return self.get_text("point/@srsName")

    @property
    def exactness (self):
        return self.get_text("exactness/@code")

    @property
    def location_class (self):
        return self.get_text("location-class/@code")

    @property
    def feature_designation (self):
        return self.get_text("feature-designation/@code")


class CodedItem (Base):
    """ Any item with a code and narrative text 
    May optionally also include @vocabulary, @vocabulary-uri, and/or @percentage

    """

    def __init__ (self, node, activity):
        super().__init__(node, activity)

    @property
    def code (self):
        """ Return the code for this object """
        return self.get_text("@code")

    @property
    def vocabulary (self):
        """ Return the code vocabulary, if defined """
        return self.get_text("@vocabulary")

    @property
    def vocabulary_uri (self):
        """ Return the code vocabulary's URI, if defined """
        return self.get_text("@vocabulary-uri")

    @property
    def narrative (self):
        """ Return any narrative text for the item """
        return self.get_narrative(".")

    @property
    def percentage (self):
        """ Return the percentage applicable to this item, if defined """
        return self.get_text("@percentage")

    @property
    def type (self):
        """ Return the @type of the item, if defined """
        return self.get_text("@type")

    @property
    def level (self):
        """ Return the @level of the item, if defined """
        return self.get_text("@level")

    def __str__ (self):
        return self.code if self.code is not None else ""


class Identifier(Base):
    """ A non-IATI activity identifier """

    def __init__ (self, node, activity):
        super().__init__(node, activity)

    @property
    def ref (self):
        """ Return text of the alternative activity identifier """
        return self.get_text("@ref")

    @property
    def type (self):
        """ Return the @type of the identifier, if defined 
        See https://iatistandard.org/en/iati-standard/203/codelists/otheridentifiertype/

        """
        return self.get_text("@type")

    @property
    def owner_org (self):
        """ Return the org that owns the identifier, if present """
        node = self.get_node("owner-org")
        if node:
            return Organisation(node, self.activity)
        else:
            return None

    

#
# Utility methods
#

def is_truthy (s):
    if not s:
        return False
    else:
        return s.strip().lower() in ['1', 'true', 'yes', 't', 'y']
