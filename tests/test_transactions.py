import logging, os, sys, unittest, xml.dom.minidom
from diterator.wrappers import Activity

class TestActivityWrapper(unittest.TestCase):

    ACTIVITY_FILE = os.path.join(os.path.dirname(__file__), "./files/activity-01.xml")

    def setUp (self):
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
        self.transaction = Activity(xml.dom.minidom.parse(self.ACTIVITY_FILE).firstChild).transactions[0]

    def test_ref (self):
        self.assertIsNone(self.transaction.ref)

    def test_humanitarian (self):
        self.assertTrue(self.transaction.humanitarian is None)

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

    def test_provider_org (self):
        self.assertEqual("Japan - Ministry of Foreign Affairs", str(self.transaction.provider_org.name))

    def test_receiver_org (self):
        # fixme needs test data
        self.assertIsNone(self.transaction.receiver_org)

    def test_disbursement_channel (self):
        # fixme needs test data
        self.assertIsNone(self.transaction.disbursement_channel)

    # sectors

    # sectors_by_vocabulary

    # recipient_countries

    # recipient_regions

    # flow-type

    # finance-type

    # aid-type

    # tied-status

    

