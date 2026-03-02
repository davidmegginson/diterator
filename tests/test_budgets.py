import logging, math, os, sys, unittest, xml.dom.minidom
from diterator.wrappers import Activity

class TestBudgetWrapper(unittest.TestCase):

    ACTIVITY_1_FILE = os.path.join(os.path.dirname(__file__), "./files/activity-01.xml")
    ACTIVITY_2_FILE = os.path.join(os.path.dirname(__file__), "./files/activity-02.xml")

    def setUp (self):
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
        self.budget = Activity(xml.dom.minidom.parse(self.ACTIVITY_1_FILE).firstChild).budgets[0]

    def test_status (self):
        self.assertEqual("2", self.budget.status)

    def test_type (self):
        self.assertEqual("1", self.budget.type)

    def test_start_date (self):
        self.assertEqual("2020-03-15", self.budget.start_date)

    def test_end_date (self):
        self.assertEqual("2021-03-14", self.budget.end_date)

    def test_currency (self):
        self.assertEqual("USD", self.budget.currency)

    def test_value_date (self):
        self.assertEqual("2020-03-01", self.budget.value_date)

    def test_value (self):
        self.assertTrue(math.isclose(1459753.72, self.budget.value))
