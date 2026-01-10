from dataclasses import dataclass

@dataclass
class OrderItem:
    order_id : int
    item_id : int
    product_id : int
    quantity : int
    list_price : float
    discount : float

    def __hash__(self):
        return hash(self.order_id)