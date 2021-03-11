import os, unittest, xml.dom.minidom
from diterator.wrappers import Activity

class TestElementWrapper(unittest.TestCase):

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

    def test_title (self):
        self.assertEqual("Promotion of Human Security through Comprehensive Health and Water, Sanitation and Hygiene (WASH) Assistance to Crisis and Conflict-Affected Populations in Somalia", str(self.activity.title))
