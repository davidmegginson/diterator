import os, unittest, xml.dom.minidom
from diterator.wrappers import Activity

class TestActivityWrapper(unittest.TestCase):

    ACTIVITY_FILE = os.path.join(os.path.dirname(__file__), "./files/activity-01.xml")

    def setUp (self):
        self.activity = Activity(xml.dom.minidom.parse(self.ACTIVITY_FILE).firstChild)

    def test_default_currency (self):
        self.assertEqual("USD", self.activity.default_currency)

    def test_default_language (self):
        self.assertEqual("en", self.activity.default_language)

    def test_humanitarian (self):
        self.assertTrue(self.activity.humanitarian)

    def test_identifier (self):
        self.assertEqual("XM-DAC-47066-DP.2154", self.activity.identifier)

    def test_reporting_org (self):
        self.assertEqual("International Organization for Migration (IOM)", str(self.activity.reporting_org))
        # test Organisation objects separately

    def test_secondary_reporter (self):
        self.assertFalse(self.activity.secondary_reporter)

    def test_participating_orgs (self):
        self.assertEqual(2, len(self.activity.participating_orgs))
        # test Organisation objects separately

    def test_participating_orgs_by_role (self):
        orgs = self.activity.participating_orgs_by_role
        self.assertEqual(1, len(orgs["1"]))
        self.assertEqual(1, len(orgs["2"]))
        # test Organisation objects separately

    def test_title (self):
        self.assertTrue(str(self.activity.title).startswith("Promotion of Human Security through Comprehensive Health "))
        # test NarrativeText objects separately

    def test_description (self):
        self.assertTrue(str(self.activity.description).startswith("The proposed project provides an "))
        # test NarrativeText objects separately

    def test_transactions (self):
        self.assertEqual(1, len(self.activity.transactions))
        # test Transaction objects separately
        
