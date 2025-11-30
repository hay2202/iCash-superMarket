from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from cashier.database import SessionLocal
from cashier.schemas.purchase_in import PurchaseIn
from cashier.services.purchase_service import PurchaseService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/purchase",
    tags=["purchase"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/customers")
def get_all_customers(db: Session = Depends(get_db)):
    """Get all existing customers from database"""
    logger.info("Received request: GET /purchase/customers")
    try:
        customers = PurchaseService.get_all_customers(db)
        logger.info(f"Returning {len(customers)} customers")
        return {"customers": customers}
    except Exception as e:
        logger.exception("Error while fetching customers")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create")
def create_purchase(p: PurchaseIn, db: Session = Depends(get_db)):
    logger.info(f"Received request: POST /purchase/create for supermarket_id={p.supermarket_id}, user_id={p.user_id}")
    try:
        purchase, is_new, user_id = PurchaseService.create_purchase(
            db=db,
            supermarket_id=p.supermarket_id,
            user_id=p.user_id,
            items=p.items_list,
        )
        logger.info(f"Purchase created successfully with ID={purchase.id}, user_id={user_id}, is_new={is_new}")

        return {
            "purchase_id": purchase.id,
            "user_id": user_id,
            "is_new": is_new,
            "total_amount": purchase.total_amount
        }

    except ValueError as e:
        logger.error(f"Validation error while creating purchase: {e}")
        raise HTTPException(status_code=400, detail=str(e))
