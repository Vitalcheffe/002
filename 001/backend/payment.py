from stripe import Stripe
from typing import Dict, Any
import logging

class PaymentService:
    def __init__(self, stripe_key: str):
        self.stripe = Stripe(stripe_key)
        self.logger = logging.getLogger(__name__)

    async def create_subscription(
        self, 
        customer_id: str, 
        plan_id: str
    ) -> Dict[str, Any]:
        try:
            subscription = await self.stripe.subscriptions.create(
                customer=customer_id,
                items=[{"plan": plan_id}],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"]
            )
            return subscription
        except Exception as e:
            self.logger.error(f"Erreur création abonnement: {str(e)}")
            raise

    async def cancel_subscription(self, subscription_id: str):
        try:
            return await self.stripe.subscriptions.delete(subscription_id)
        except Exception as e:
            self.logger.error(f"Erreur annulation abonnement: {str(e)}")
            raise 