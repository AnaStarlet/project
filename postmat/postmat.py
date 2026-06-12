class PostalBox:
    def __init__(self, cell_count, notification_client):
        self.cell_count = cell_count
        self.cells = [None] * cell_count
        self.order_to_cell = {}
        self.code_to_cell = {}
        self.notification_client = notification_client

    def place_order(self, order_id, user_phone):

        if order_id in self.order_to_cell:
            raise ValueError(f"заказ {order_id} уже есть в ячейке {self.order_to_cell[order_id]}")

        for cell_number in range(self.cell_count):
            if self.cells[cell_number] is None:
                self.cells[cell_number] = order_id
                self.order_to_cell[order_id] = cell_number
                message = f"заказ {order_id} в ячейке {cell_number}"
                receive_code = self.notification_client.send_sms(user_phone, message)
                self.code_to_cell[receive_code] = order_id
                return cell_number

        raise ValueError(f"нет свободных ячеек для заказа {order_id}")
    def get_order(self, receive_code):
        if receive_code not in self.code_to_cell:
            print(f"неверный код: {receive_code}")
            return None
        order_id = self.code_to_cell[receive_code]
        cell_number = self.order_to_cell[order_id]
        self.cells[cell_number] = None
        del self.order_to_cell[order_id]
        del self.code_to_cell[receive_code]
        return cell_number

class UserNotificationApi:
    def send_sms(self, phone: str, message: str) -> str:
        import random
        code = str(random.randint(1000, 9999))
        print(f"СМС на {phone}: {message} код: {code}")
        return code

if __name__ == "__main__":
    postamat = PostalBox(5, UserNotificationApi())

    cell = postamat.place_order(12345, "+123456789")
    print(f"курьер: заказ 12345 в ячейку {cell}")

    result = postamat.get_order("9999")
    print(f"результат получения: ячейка {result}")


