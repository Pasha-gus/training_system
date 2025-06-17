import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course_name):
    product = stripe.Product.create(name=course_name)
    return product.get("id")


def create_stripe_price(course_price, stripe_product_id):
    """Создает цену в stripe."""
    course_price_float = float(course_price)
    return stripe.Price.create(currency="rub", unit_amount=int(course_price_float * 100), product=stripe_product_id)


def create_stripe_session(stripe_price):
    """Создает сессию на оплату в stripe."""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": stripe_price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
