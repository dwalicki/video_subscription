from lib2to3.pytree import Base
import string
import stripe
import random
import string
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from video_subscription_service.content.models import Pricing, Subscription

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY

def randomStringWithDigitsAndSymbols(stringLength=20):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(
        random.choice(password_characters) for i in range(stringLength))

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username="admin2").exists():
            if settings.DEBUG:
                password = "admin"
            else:
                password = randomStringWithDigitsAndSymbols()
            user = User.objects.create_superuser(
                "admin2", "admin@test.com", password
            )
            free_trial_pricing = Pricing.objects.get(name='Free Trial')
            subscription = Subscription.objects.create(
                user=user, 
                pricing=free_trial_pricing
            )
            stripe_customer = stripe.Customer.create(
                email=user.email,
            )
            stripe_subscription = stripe.Subscription.create(
                customer=stripe_customer["id"],
                items=[{"price": free_trial_pricing.stripe_price_id }],
                    trial_period_days=28
            )
            subscription.status = stripe_subscription["status"]
            subscription.stripe_subscription_id = stripe_subscription["id"]
            subscription.save()
            user.stripe_customer_id = stripe_customer["id"]
            user.save()
