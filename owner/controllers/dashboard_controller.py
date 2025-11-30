from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from owner.db import SessionLocal
from owner.services.dashboard_service import PurchaseService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/dashboard",
    tags=["owner"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/unique-buyers")
def unique_buyers(db: Session = Depends(get_db)):
    try:
        logger.info("Received request: GET /dashboard/unique-buyers")
        count = PurchaseService.unique_buyers(db)
        logger.info(f"Returning unique buyers count: {count}")
        return {"unique_buyers": count}
    except Exception as e:
        logger.exception("Error while fetching unique buyers")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/loyal-buyers")
def loyal_buyers(db: Session = Depends(get_db)):
    try:
        logger.info("Received request: GET /dashboard/loyal-buyers")
        rows = PurchaseService.loyal_buyers(db)
        logger.info(f"Returning loyal buyers rows: {len(rows)}")
        return {"loyal_buyers": rows}
    except Exception as e:
        logger.exception("Error while fetching loyal buyers")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top-products")
def top_products(db: Session = Depends(get_db)):
    try:
        logger.info("Received request: GET /dashboard/top-products")
        rows = PurchaseService.top_products(db)
        logger.info(f"Returning top products rows: {len(rows)}")
        return {"top_products": rows}
    except Exception as e:
        logger.exception("Error while fetching top products")
        raise HTTPException(status_code=500, detail=str(e))
