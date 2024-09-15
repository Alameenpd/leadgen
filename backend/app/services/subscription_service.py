from sqlalchemy.orm import Session
from app.models.user import User
from datetime import datetime, timedelta
import requests
from app.core.config import settings

PLAN_LIMITS = {
    "basic": {"leads": 1000, "dms": 2500, "campaigns": 20},
    "pro": {"leads": 5000, "dms": 5000, "campaigns": 50},
    "enterprise": {"leads": 20000, "dms": 10000, "campaigns": float('inf')}
}

def get_user_limits(user: User):
    return PLAN_LIMITS.get(user.subscription_plan, {"leads": 0, "dms": 0, "campaigns": 0})

def check_user_limit(user: User, limit_type: str):
    limits = get_user_limits(user)
    return limits.get(limit_type, 0)

def update_user_subscription(db: Session, user: User, plan: str, duration_months: int = 1):
    user.subscription_plan = plan
    user.subscription_start_date = datetime.utcnow()
    user.subscription_end_date = user.subscription_start_date + timedelta(days=30*duration_months)
    db.commit()

def create_lemonsqueezy_checkout(plan: str, user_email: str):
    store_id = settings.LEMONSQUEEZY_STORE_ID
    variant_id = settings.LEMONSQUEEZY_VARIANT_IDS[plan]
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.LEMONSQUEEZY_API_KEY}"
    }
    
    payload = {
        "data": {
            "type": "checkouts",
            "attributes": {
                "custom_price": None,
                "product_options": {
                    "name": "enabled",
                    "description": "enabled",
                    "media": "enabled",
                    "redirect_url": f"{settings.FRONTEND_URL}/subscription/success"
                },
                "checkout_data": {
                    "email": user_email
                }
            },
            "relationships": {
                "store": {
                    "data": {
                        "type": "stores",
                        "id": store_id
                    }
                },
                "variant": {
                    "data": {
                        "type": "variants",
                        "id": variant_id
                    }
                }
            }
        }
    }
    
    response = requests.post(
        "https://api.lemonsqueezy.com/v1/checkouts",
        json=payload,
        headers=headers
    )
    
    if response.status_code == 201:
        return response.json()["data"]["attributes"]["url"]
    else:
        raise Exception("Failed to create LemonSqueezy checkout")

def handle_lemonsqueezy_webhook(db: Session, event_name: str, data: dict):
    if event_name == "order_created":
        user_email = data["user_email"]
        plan = data["product_name"].lower()
        user = db.query(User).filter(User.email == user_email).first()
        if user:
            update_user_subscription(db, user, plan)
            user.lemonsqueezy_customer_id = data["customer_id"]
            db.commit()
    elif event_name == "subscription_cancelled":
        customer_id = data["customer_id"]
        user = db.query(User).filter(User.lemonsqueezy_customer_id == customer_id).first()
        if user:
            user.subscription_end_date = datetime.utcnow()
            db.commit()