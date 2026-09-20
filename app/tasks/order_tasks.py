from datetime import datetime


def send_order_confirmation(order_id: int, user_id: int):
    print(
        f"Order confirmation: "
        f"Order ID={order_id}, "
        f"User ID={user_id}, "
        f"Time={datetime.now()}"
    )