import uuid, logging
from datetime import datetime
from sqlalchemy.orm import Session
from cashier.models.user import User
from cashier.models.product import Product
from cashier.models.purchase import Purchase

logger = logging.getLogger(__name__)

class PurchaseService:

    @classmethod
    def get_all_customers(cls, db: Session):
        """Get all existing customers from database"""
        logger.info("Fetching all customers from database")
        customers = db.query(User.user_id).all()
        logger.debug(f"Found {len(customers)} customers")
        return [customer[0] for customer in customers]

    @classmethod
    def get_or_create_user(cls, db: Session, user_id: str = None):
        """Get existing user or create new one with auto-generated ID"""
        logger.info(f"get_or_create_user called with user_id={user_id}")

        # If user_id is provided, try to find an existing user
        if user_id:
            user = db.query(User).filter(User.user_id == user_id).first()
            if user:
                logger.info(f"Existing user found: {user.user_id}")
                return user, False

        logger.info("No user found, generating a new user ID")
        # Create new user with auto-generated ID
        generated_id = cls._generate_unique_user_id(db)
        new_user = User(user_id=generated_id)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"New user created: {new_user.user_id}")
        return new_user, True

    @classmethod
    def _generate_unique_user_id(cls, db: Session):
        """Generate a unique user_id for new customers"""
        logger.info("Generating unique user_id")
        while True:
            new_id = str(uuid.uuid4())
            # Check if this ID already exists
            existing = db.query(User).filter(User.user_id == new_id).first()
            if not existing:
                logger.debug(f"Generated unique user_id: {new_id}")
                return new_id

    @classmethod
    def calculate_total(cls, db: Session, items: list[str]):
        logger.debug(f"Calculating total for items: {items}")
        total = 0
        for item in items:
            product = db.query(Product).filter(Product.product_name == item).first()
            if not product:
                logger.error(f"Unknown product: {item}")
                raise ValueError(f"Unknown product: {item}")
            total += product.unit_price
        logger.debug(f"Total calculated: {total}")
        return total

    @classmethod
    def create_purchase(cls, db: Session, supermarket_id: str, user_id: str = None, items: list[str] = None):
        logger.info(f"Creating purchase for supermarket_id={supermarket_id}, user_id={user_id}")
        user, is_new = cls.get_or_create_user(db, user_id)
        total = cls.calculate_total(db, items)
        logger.info(f"Purchase total: {total}")

        purchase = Purchase(
            id=str(uuid.uuid4()),
            supermarket_id=supermarket_id,
            user_id=user.user_id,
            items_list=",".join(items),
            total_amount=total,
            timestamp=datetime.utcnow()
        )

        logger.debug(f"Saving purchase {purchase} for user {user.user_id}")
        db.add(purchase)
        db.commit()
        db.refresh(purchase)
        logger.info(f"Purchase created successfully: {purchase.id}")

        return purchase, is_new, user.user_id
