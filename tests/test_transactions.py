import os, unittest, xml.dom.minidom
from diterator.wrappers import Activity

class TestActivityWrapper(unittest.TestCase):

    ACTIVITY_FILE = os.path.join(os.path.dirname(__file__), "./files/activity-01.xml")

    def setUp (self):
        self.transaction = Activity(xml.dom.minidom.parse(self.ACTIVITY_FILE).firstChild).transactions[0]

    def test_ref (self):
        self.assertIsNone(self.transaction.ref)

    def test_humanitarian (self):
        self.assertIsNone(self.transaction.humanitarian)

    def test_date (self):
        self.assertEqual("2020-03-01", self.transaction.date)

    def test_type (self):
        self.assertEqual("11", self.transaction.type)

    def test_value (self):
        self.assertEqual(1459753.72, self.transaction.value)

    def test_currency (self):
        self.assertEqual("USD", self.transaction.currency)

    def test_value_date (self):
        self.assertEqual("2020-03-01", self.transaction.value_date)

    def test_description (self):
        self.assertIsNone(self.transaction.description)

