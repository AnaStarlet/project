import unittest
from unittest.mock import Mock

from postamat import PostalBox, UserNotificationApi

class TestPostamat(unittest.TestCase):

    def test_place_order_success(self): #успешно в постамат
        mock_client = Mock(spec=UserNotificationApi)
        mock_client.send_sms.return_value = "2345"
        postamat = PostalBox(3, mock_client)
        cell = postamat.place_order(12345, "+79001234567")
        self.assertEqual(cell, 0)
        mock_client.send_sms.assert_called_once()

    def test_duplicate_order_id(self): #дубликат
        mock_client = Mock(spec=UserNotificationApi)
        mock_client.send_sms.return_value = "2345"
        postamat = PostalBox(3, mock_client)
        postamat.place_order(12345, "+79001234567")
        with self.assertRaises(ValueError):
            postamat.place_order(12345, "+79001234567")

    def test_wrong_code(self): #неверный код
        mock_client = Mock(spec=UserNotificationApi)
        mock_client.send_sms.return_value = "2345"
        postamat = PostalBox(3, mock_client)
        postamat.place_order(12345, "+79001234567")
        cell = postamat.get_order("9999")
        self.assertIsNone(cell)

    def test_no_free_cells(self): #непустая ячейка
        mock_client = Mock(spec=UserNotificationApi)
        postamat = PostalBox(1, mock_client)
        postamat.place_order(111, "+79001111111")
        with self.assertRaises(ValueError):
            postamat.place_order(222, "+79002222222")

    def test_get_order_success(self): #верный номер
        mock_client = Mock(spec=UserNotificationApi)
        mock_client.send_sms.return_value = "2345"
        postamat = PostalBox(3, mock_client)
        postamat.place_order(12345, "+79001234567")
        cell = postamat.get_order("2345")
        self.assertEqual(cell, 0)

if __name__ == '__main__':
    unittest.main()





