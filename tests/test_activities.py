import logging, os, sys, unittest, xml.dom.minidom
from diterator.wrappers import Activity

class TestActivityWrapper(unittest.TestCase):

    ACTIVITY_FILE = os.path.join(os.path.dirname(__file__), "./files/activity-01.xml")

    def setUp (self):
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
        self.activity = Activity(xml.dom.minidom.parse(self.ACTIVITY_FILE).firstChild)

    def test_default_currency (self):
        self.assertEqual("USD", self.activity.default_currency)

    def test_default_language (self):
        self.assertEqual("en", self.activity.default_language)

    def test_humanitarian (self):
        self.assertTrue(self.activity.humanitarian is True)

    # @hierarchy

    # @linked-data-uri

    # @budget-not-provided

    def test_identifier (self):
        self.assertEqual("XM-DAC-00000-0000", self.activity.identifier)

    def test_reporting_org (self):
        self.assertEqual("Test Org", str(self.activity.reporting_org))

    def test_secondary_reporter (self):
        self.assertTrue(self.activity.secondary_reporter is None)

    def test_title (self):
        self.assertEqual("Test activity title", str(self.activity.title))

    def test_description (self):
        self.assertTrue(str(self.activity.description).startswith("Test activity description"))

    def test_participating_orgs (self):
        self.assertEqual(2, len(self.activity.participating_orgs))

    def test_other_identifiers (self):
        self.assertEqual(1, len(self.activity.other_identifiers))

    def test_participating_orgs_by_role (self):
        orgs = self.activity.participating_orgs_by_role
        self.assertEqual(1, len(orgs["1"]))
        self.assertEqual(1, len(orgs["2"]))

    def test_participating_orgs_by_type (self):
        orgs = self.activity.participating_orgs_by_type
        self.assertEqual(1, len(orgs["10"]))
        self.assertEqual(1, len(orgs["40"]))

    def test_activity_status (self):
        self.assertEqual("2", self.activity.activity_status)

    def test_is_active (self):
        self.assertTrue(self.activity.is_active is True)

    def test_start_date_planned (self):
        self.assertEqual("2020-03-15", self.activity.start_date_planned)

    def test_start_date_actual (self):
        self.assertEqual("2020-03-16", self.activity.start_date_actual)

    def test_end_date_planned (self):
        self.assertEqual("2021-03-14", self.activity.end_date_planned)

    def test_end_date_actual (self):
        self.assertEqual("2021-03-15", self.activity.end_date_actual)

    # contact-info

    def test_activity_scope (self):
        self.assertEqual("5", self.activity.activity_scope)

    def test_recipient_countries (self):
        self.assertEqual(1, len(self.activity.recipient_countries))

    def test_recipient_regions (self):
        self.assertEqual(1, len(self.activity.recipient_regions))

    def test_sectors (self):
        self.assertEqual(3, len(self.activity.sectors))

    def test_sectors_by_vocabulary (self):
        self.assertEqual(1, len(self.activity.sectors_by_vocabulary["1"]))
        self.assertEqual(1, len(self.activity.sectors_by_vocabulary["98"]))
        self.assertEqual(1, len(self.activity.sectors_by_vocabulary["99"]))

    def test_tags (self):
        self.assertEqual(2, len(self.activity.tags))

    def test_tags_by_vocabulary (self):
        self.assertEqual(2, len(self.activity.tags_by_vocabulary["1"]))

    # country-budget-items

    def test_humanitarian_scopes (self):
        self.assertEqual(1, len(self.activity.humanitarian_scopes))

    def test_humanitarian_scopes_by_type (self):
        self.assertEqual(1, len(self.activity.humanitarian_scopes_by_type["1"]))

    def test_humanitarian_scopes_by_vocabulary (self):
        self.assertEqual(1, len(self.activity.humanitarian_scopes_by_vocabulary["1-2"]))

    def test_policy_markers (self):
        self.assertEqual(2, len(self.activity.policy_markers))

    def test_policy_markers_by_significance (self):
        self.assertEqual(2, len(self.activity.policy_markers_by_significance["1"]))

    def test_policy_markers_by_vocabulary (self):
        self.assertEqual(2, len(self.activity.policy_markers_by_vocabulary["1"]))

    def test_collaboration_type (self):
        # fixme - example needed
        self.assertIsNone(self.activity.collaboration_type)

    def test_default_flow_type (self):
        # fixme - example needed
        self.assertIsNone(self.activity.default_flow_type)

    def test_default_finance_type (self):
        # fixme - example needed
        self.assertIsNone(self.activity.default_finance_type)

    def test_default_aid_types (self):
        # fixme - example needed
        self.assertEqual(0, len(self.activity.default_aid_types))

    def test_default_aid_types_by_vocabulary (self):
        # fixme - example needed
        self.assertEqual(0, len(self.activity.default_aid_types_by_vocabulary))

    def test_default_tied_status (self):
        # fixme - example needed
        self.assertIsNone(self.activity.default_tied_status)

    # budget

    # planned-disbursement

    # capital-spend

    def test_transactions (self):
        self.assertEqual(1, len(self.activity.transactions))

    # transactions_by_type
        
    # document-link

    def test_related_activities (self):
        self.assertEqual(2, len(self.activity.related_activities))
        self.assertEqual("1", self.activity.related_activities[0].type)
        self.assertEqual("XXX-YYY-ZZZ", self.activity.related_activities[0].ref)

    def test_related_activities_by_type (self):
        data = self.activity.related_activities_by_type
        self.assertEqual(1, len(data["1"]))
        self.assertEqual("1", data["1"][0].type)
        self.assertEqual(1, len(data["3"]))
        self.assertEqual("3", data["3"][0].type)

    # legacy-data

    # conditions

    # result

    # crs-add

    # fss
