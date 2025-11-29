import stripe
from fastapi import HTTPException
from ..config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY   # ВАЖНО!


class StripeService:
    @staticmethod
    def create_checkout_session(order):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {"name": f"Order #{order.id}"},
                            "unit_amount": int(order.total_price * 100),  # cents
                        },
                        "quantity": 1,
                    }
                ],
                success_url=f"https://your-site.com/success?order_id={order.id}",
                cancel_url=f"https://your-site.com/cancel?order_id={order.id}",
                metadata={"order_id": order.id},
            )

            return session.url

        except Exception as e:
            raise HTTPException(500, str(e))
