from fastapi import HTTPException
from app.db_connect.models.orders import Orders
from app.db_connect.models.tracking import Tracking
from uuid import UUID,uuid4
import datetime

def create_tracking(order_id : UUID, db):
    order = db.query(Orders).filter(Orders.order_id == order_id ).first()
    if not order:
        raise HTTPException(status_code=404, detail="order not found")
    tracking_check = db.query(Tracking).filter(Tracking.order_id == order_id).first()
    if tracking_check:
        raise HTTPException(status_code=409 , detail= "traking for order id already created")
    tracking_id = uuid4()
    odered_date = datetime.datetime.now()
    shipment_date = odered_date + datetime.timedelta(days=3)
    delevery_date = shipment_date+ datetime.timedelta(days = 3)
    tracking = Tracking(
        tracking_id = tracking_id,
        order_id = order_id,
        status = "odered",
        odered_date = odered_date,
        shipment_date = shipment_date,
        delevery_date = delevery_date
    )
    db.add(tracking)
    db.commit()
    return "tracking added successfully"

def get_current_tracking_status(tracking_id : UUID,  db):
    tracking = db.query(Tracking).filter(Tracking.tracking_id == tracking_id).first()
    if not tracking:
        raise HTTPException(status_code=404, detail="no traking found")
    output = {"order_id":tracking.order_id,
              "current_status":tracking.status,
              "shipment":{"status":"","date":""},
              "delevery":{"status":"","date":""}
              }
    ## Shipment status
    if tracking.shipment_date < datetime.datetime.now():
        output["current_status"] = "shipment completed"
        output["shipment"]['status'] = "shipped"
        output["shipment"]['date'] = tracking.shipment_date
    else:
        output["shipment"]['status'] = "pending"
        output["shipment"]['date'] = tracking.shipment_date
    
    ## Delevery status 
    if tracking.delevery_date < datetime.datetime.now():
        output["current_status"] = "delevered"
        output["delevery"]['status'] = "delevered"
        output["delevery"]['date'] = tracking.delevery_date
    else:
        output["delevery"]['status'] = "pending"
        output["delevery"]['date'] = tracking.delevery_date

    return output

def change_shipment_date(tracking_id : UUID,shipment_date :datetime,db):
    tracking = db.query(Tracking).filter(Tracking.tracking_id == tracking_id).first()
    if not tracking:
        raise HTTPException(status_code=404, detail="no traking found")
    current_shipment_date = shipment_date or datetime.datetime.now()
    tracking.shipment_date = current_shipment_date
    tracking.delevery_date = current_shipment_date + datetime.timedelta(days=3)
    db.commit()
    return "shipment date changed"

def change_delevery_date(tracking_id : UUID,delevery_date :datetime,db):
    tracking = db.query(Tracking).filter(Tracking.tracking_id == tracking_id).first()
    if not tracking:
        raise HTTPException(status_code=404, detail="no traking found")
    tracking.delevery_date = delevery_date or datetime.datetime.now()
    db.commit()
    return "delevery date changed"

