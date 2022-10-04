
from query import Query, get_date_from_str, is_valid_date
import unittest

class TestQuery(unittest.TestCase):

    def test_valid_date_checker_good_input(self):
        date = "2000-01-01"
        self.assertTrue(is_valid_date(date))

    def test_valid_date_checker_bad_input1(self):
        date = "2000-41-01"
        self.assertFalse(is_valid_date(date))

    def test_valid_date_checker_bad_input2(self):
        date = "01-01-2000"
        self.assertFalse(is_valid_date(date))

    def test_valid_date_checker_bad_input3(self):
        date = "01-01-0001"
        self.assertFalse(is_valid_date(date))

    def test_valid_date_checker_bad_input4(self):
        date = "orange"
        self.assertFalse(is_valid_date(date))

    def test_valid_date_checker_bad_input5(self):
        date = ""
        self.assertFalse(is_valid_date(date))

    def test_gdfs_good_input(self):
        date_str = "2000-01-01"
        self.assertEqual(get_date_from_str(date_str), (2000, 1, 1))

    def test_gdfs_bad_input1(self):
        date_str = "elephant"
        self.assertRaises(ValueError, get_date_from_str, date_str)

    def test_gdfs_bad_input2(self):
        date_str = "elephant-giraff-tiger"
        self.assertRaises(ValueError, get_date_from_str, date_str)

    def test_gdfs_bad_input3(self):
        date_str = "02-02-2002"
        self.assertRaises(ValueError, get_date_from_str, date_str)

    def test_gdfs_bad_input4(self):
        date_str = "03-03-0003"
        self.assertRaises(ValueError, get_date_from_str, date_str)

    def test_query_items_sold(self):
        date = "2019-08-01"
        query = Query()
        self.assertEqual(query.items_sold, 2895)

    # Etc. for the others, they're time consuming to compute by hand, and prone to error
    # but you could test it that way.


# My first time using unittest and doing proper unittest in general
# normally just resort to testing in the console and good old print
# statements all over the place - though I'm aware that's not exactly
# best practice, esp. in prod code.
# Not sure how to test the Query class other than to use it, and that seems
# to work fine, not sure how the integration testing works but I have
# performed some manual checks of the values the program returns and they seem
# accurate

if __name__ == "__main__":
    unittest.main()
