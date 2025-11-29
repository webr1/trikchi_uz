from fastapi import APIRouter, HTTPException, Request, Depends
import stripe
from backend.app.database import get_db
from backend.app.services.order_service import OrderService
from backend.app.config import settings   # секреты берем из .env

router = APIRouter(prefix="/stripe", tags=["Stripe"])

# Секрет Stripe (не хардкодим!)
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


@router.post("/webhook")
async def stripe_webhook(request: Request, db=Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    # 1. Проверка подписи Stripe (обязательно)
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        print("❌ Invalid signature:", str(e))
        raise HTTPException(400, "Invalid signature")

    # 2. Логирование для тестов
    print("🔔 Stripe Webhook received")
    print("Event type:", event["type"])

    # 3. Обработка успешной оплаты
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = session["metadata"]["order_id"]

        print("✔ Payment Completed")
        print("Order ID:", order_id)

        # ---- Пока НЕ обновляем заказ (как ты просил) ----
        # Если будет нужно — включим:
        #
        # service = OrderService(db)
        # order = service.repo.get_order(order_id)
        # service.set_status(order_id, "paid", user_id=order.user_id)

    return {"success": True}
