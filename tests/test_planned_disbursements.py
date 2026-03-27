import logging, math, os, sys, unittest, xml.dom.minidom
from diterator.wrappers import Activity

class TestPlannedDisbursementWrapper(unittest.TestCase):

    ACTIVITY_1_FILE = os.path.join(os.path.dirname(__file__), "./files/activity-01.xml")
    ACTIVITY_2_FILE = os.path.join(os.path.dirname(__file__), "./files/activity-02.xml")

    def setUp (self):
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
        self.planned_disbursement = Activity(xml.dom.minidom.parse(self.ACTIVITY_1_FILE).firstChild).planned_disbursements[0]

    def test_type (self):
        self.assertEqual("1", self.planned_disbursement.type)

    def test_start_date (self):
        self.assertEqual("2026-01-01", self.planned_disbursement.start_date)

    def test_end_date (self):
        self.assertEqual("2026-03-31", self.planned_disbursement.end_date)

    def test_currency (self):
        self.assertEqual("USD", self.planned_disbursement.currency)

    def test_value_date (self):
        self.assertEqual("2026-01-01", self.planned_disbursement.value_date)

    def test_value (self):
        self.assertTrue(math.isclose(100000.0, self.planned_disbursement.value))

    def test_provider_org (self):
        provider_org = self.planned_disbursement.provider_org
        self.assertIsNotNone(provider_org)
        self.assertEqual("XM-DAC-701-2", provider_org.ref)

    def test_receiver_org (self):
        receiver_org = self.planned_disbursement.receiver_org
        self.assertIsNotNone(receiver_org)
        self.assertEqual("FOO", receiver_org.ref)
