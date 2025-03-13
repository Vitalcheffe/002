from stripe import Stripe
from typing import Dict, Optional
import logging

class PaymentService:
    def __init__(self):
        self.stripe = Stripe(os.getenv("STRIPE_SECRET_KEY"))
        self.logger = logging.getLogger(__name__)
        self.plans = {
            "basic": {
                "price_id": "price_H2jn2k...",
                "features": ["résumés", "quiz basiques"],
                "limits": {"requests_per_day": 50}
            },
            "pro": {
                "price_id": "price_K9mn3j...",
                "features": ["tout basic + cartes mentales", "audio"],
                "limits": {"requests_per_day": 200}
            },
            "enterprise": {
                "price_id": "price_L8kp4h...",
                "features": ["tout pro + API access", "support prioritaire"],
                "limits": {"requests_per_day": -1}  # illimité
            }
        }

    async def create_subscription(self, user_id: str, plan_id: str) -> Dict:
        try:
            # Création du client Stripe s'il n'existe pas
            customer = await self._get_or_create_customer(user_id)
            
            # Création de l'abonnement
            subscription = await self.stripe.subscriptions.create(
                customer=customer.id,
                items=[{"price": self.plans[plan_id]["price_id"]}],
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"],
                metadata={"user_id": user_id}
            )

            return {
                "subscription_id": subscription.id,
                "client_secret": subscription.latest_invoice.payment_intent.client_secret
            }
        except Exception as e:
            self.logger.error(f"Erreur création abonnement: {str(e)}")
            raise

    async def handle_webhook(self, event_data: Dict) -> None:
        """Gestion des webhooks Stripe"""
        event_type = event_data["type"]
        
        handlers = {
            "customer.subscription.created": self._handle_subscription_created,
            "customer.subscription.updated": self._handle_subscription_updated,
            "customer.subscription.deleted": self._handle_subscription_deleted,
            "invoice.paid": self._handle_invoice_paid,
            "invoice.payment_failed": self._handle_payment_failed
        }

        if event_type in handlers:
            await handlers[event_type](event_data["data"]["object"]) 