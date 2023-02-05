from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request
from .base import BaseService
from ..controllers import OrderController

order = Blueprint('order', __name__)

order_service = BaseService()

@order.route('/', methods=POST)
def create_order():
    return order_service.create(OrderController.create)

@order.route('/', methods=PUT)
def update_order():
    return order_service.update(OrderController.update)

@order.route('/id/<_id>', methods=GET)
def get_order_by_id(_id: int):
    return order_service.get_by_id(_id, OrderController.get_by_id)

@order.route('/', methods=GET)
def get_orders():
    return order_service.get_all(OrderController.get_all)
