import unittest
from postmat import PostalBox, UserNotificationApi

class TestPostamat(unittest.TestCase):

    def test_place_order_success(self):
        postamat = PostalBox(3, UserNotificationApi())
        result = postamat.place_order(12345, "+79001234567")
        self.assertTrue(result)

    def test_get_order_success(self):
        postamat = PostalBox(3, UserNotificationApi())
        postamat.place_order(12345, "+79001234567")
        cell = postamat.get_order("2345")
        self.assertEqual(cell, 0)

    def test_no_free_cells(self):
        postamat = PostalBox(1, UserNotificationApi())
        postamat.place_order(111, "+79001111111")
        result = postamat.place_order(222, "+79002222222")
        self.assertFalse(result)

    def test_wrong_code(self):
        postamat = PostalBox(3, UserNotificationApi())
        postamat.place_order(12345, "+79001234567")
        cell = postamat.get_order("9999")
        self.assertIsNone(cell)

if __name__ == '__main__':
    unittest.main()