from backend.app.database import SessionLocal
from backend.app.models import Order, OrderItem

db = SessionLocal()

order = Order(user_id=1, total_price=30000)
db.add(order)
db.commit()
db.refresh(order)

item = OrderItem(order_id=order.id, product_id=1, price=15000, quantity=2)
db.add(item)
db.commit()

print("Created order id:", order.id)
