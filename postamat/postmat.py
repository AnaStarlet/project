class PostalBox:
    def __init__(self, cell_count, notification_client):
        self.cell_count = cell_count
        self.cells = [None] * cell_count
        self.order_to_cell = {}
        self.code_to_cell = {}
        self.notification_client = notification_client

    def place_order(self, order_id, user_phone):
        for cell_number  in range(self.cell_count):
            if self.cells[cell_number] is None:
                self.cells[cell_number] = order_id
                self.order_to_cell[order_id] = cell_number
                receive_code = str(order_id)[-4:]
                self.code_to_cell[receive_code] = order_id
                message = f"заказ {order_id} в ячейке {cell_number} код: {receive_code}"
                self.notification_client.send_sms(user_phone, message)
                return True
        print(f"нет свободных ячеек для заказа {order_id}")
        return False
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
    def send_sms(self, phone: str, message: str):
        print(f"СМС на {phone}: {message}")

if __name__ == "__main__":
    postamat = PostalBox(5, UserNotificationApi())
    postamat.place_order(12345, "+123456789")
    postamat.place_order(67890, "+987654321")
    postamat.get_order("9999")
    postamat.get_order("2345")


