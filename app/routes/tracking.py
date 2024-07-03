from fastapi import APIRouter, Request, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from app.db_connect.database import get_db
from app.services import tracking

router = APIRouter(prefix="/tracking", tags=['tracking'])


@router.post("/{order_id}")
def add_tracking_to_order(order_id : UUID, db : Session = Depends(get_db)):
    return tracking.create_tracking(order_id=order_id, db = db)

@router.put("/{tracking_id}/shipment")
def change_shipment_status(tracking_id : UUID, db : Session = Depends(get_db)):
    return tracking.change_shipment_date(tracking_id=tracking_id,shipment_date = None, db = db)

@router.put("/{tracking_id}/delevery")
def change_delevery_status(tracking_id : UUID, db : Session = Depends(get_db)):
    return tracking.change_delevery_date(tracking_id=tracking_id,delevery_date=None, db = db)

@router.get("/{tracking_id}")
def get_tracking_by_id(tracking_id : UUID, db: Session = Depends(get_db)):
    return tracking.get_current_tracking_status(tracking_id= tracking_id, db = db)