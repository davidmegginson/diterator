import logging, os, sys, unittest, xml.dom.minidom
from diterator.wrappers import Activity

class TestActivityWrapper(unittest.TestCase):

    ACTIVITY_1_FILE = os.path.join(os.path.dirname(__file__), "./files/activity-01.xml")
    ACTIVITY_2_FILE = os.path.join(os.path.dirname(__file__), "./files/activity-02.xml")

    def setUp (self):
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
        self.transaction1 = Activity(xml.dom.minidom.parse(self.ACTIVITY_1_FILE).firstChild).transactions[0]
        self.transaction2 = Activity(xml.dom.minidom.parse(self.ACTIVITY_2_FILE).firstChild).transactions[0]

    def test_ref (self):
        self.assertIsNone(self.transaction1.ref)

    def test_humanitarian (self):
        self.assertTrue(self.transaction1.humanitarian is None)

    def test_date (self):
        self.assertEqual("2020-03-01", self.transaction1.date)

    def test_type (self):
        self.assertEqual("11", self.transaction1.type)

    def test_value (self):
        self.assertEqual(1459753.72, self.transaction1.value)

    def test_currency (self):
        self.assertEqual("USD", self.transaction1.currency)

    def test_missing_currency (self):
        self.assertIsNone(self.transaction2.currency) # currency not specified as default or in transaction

    def test_value_date (self):
        self.assertEqual("2020-03-01", self.transaction1.value_date)

    def test_description (self):
        self.assertIsNone(self.transaction1.description)

    def test_provider_org (self):
        self.assertEqual("Japan - Ministry of Foreign Affairs", str(self.transaction1.provider_org.name))

    def test_receiver_org (self):
        # fixme needs test data
        self.assertIsNone(self.transaction1.receiver_org)

    def test_disbursement_channel (self):
        self.assertEqual("2", self.transaction1.disbursement_channel)

    # sectors

    # sectors_by_vocabulary

    # recipient_countries

    # recipient_regions

    def test_flow_type (self):
        self.assertEqual("10", self.transaction1.flow_type)

    def test_finance_type (self):
        self.assertEqual("110", self.transaction1.finance_type)

    def test_aid_type (self):
        self.assertEqual("1", self.transaction1.aid_types[0].vocabulary)
        self.assertEqual("B03", self.transaction1.aid_types[0].code)

    def test_aid_types_by_vocabulary (self):
        self.assertEqual("B03", self.transaction1.aid_types_by_vocabulary["1"][0].code)

    def test_tied_status (self):
        self.assertEqual("5", self.transaction1.tied_status)
