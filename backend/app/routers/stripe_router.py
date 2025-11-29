from fastapi import APIRouter, Depends, HTTPException
from backend.app.database import get_db
from backend.app.services.order_service import OrderService
from backend.app.services.stripe_service import StripeService

router = APIRouter(prefix="/stripe", tags=["Stripe"])


@router.post("/create-session/{order_id}")
def create_session(order_id: int, db=Depends(get_db)):
    order = OrderService(db).repo.get_order(order_id)
    if not order:
        raise HTTPException(404, "Order not found")

    url = StripeService.create_checkout_session(order)
    return {"checkout_url": url}
