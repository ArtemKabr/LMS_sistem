# materials/services/stripe_service.py — сервисы Stripe
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course):
    """Создаёт продукт в Stripe на основе объекта курса."""
    product = stripe.Product.create(
        name=course.title,
        description=getattr(course, "description", "") or "",
    )
    return product.id


def create_stripe_price(product_id: str, amount):
    """Создаёт цену в Stripe, учитывая перевод суммы в минимальные единицы (×100)."""
    price = stripe.Price.create(
        unit_amount=int(amount * 100),
        currency="usd",
        product=product_id,
    )
    return price.id


def create_checkout_session(price_id: str) -> dict:
    """Создаёт сессию оплаты Stripe и возвращает её id и ссылку на оплату."""
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url="http://127.0.0.1:8000/success",
        cancel_url="http://127.0.0.1:8000/cancel",
    )
    return {"id": session.id, "url": session.url}
