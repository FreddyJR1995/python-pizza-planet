from typing import Any, List, Optional, Sequence
from sqlalchemy.sql import text, column, func, desc, extract
from datetime import datetime

from .models import Beverage, Ingredient, Order, OrderDetail, Size, OrderBeverage, db
from .serializers import (IngredientSerializer, OrderSerializer,
                          SizeSerializer, BeverageSerializer, ma)


class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []

class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []

class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]):
        new_order = cls.model(**order_data)
        new_order.date = datetime.now() if new_order.date is None else datetime.strptime(new_order.date, '%Y-%m-%d %H:%M:%S')
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all((OrderDetail(order_id=new_order._id, ingredient_id=ingredient._id, ingredient_price=ingredient.price)
                             for ingredient in ingredients))
        cls.session.add_all((OrderBeverage(order_id=new_order._id, beverage_id=beverage._id, beverage_price=beverage.price)
                             for beverage in beverages))
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')


class IndexManager(BaseManager):

    @classmethod
    def test_connection(cls):
        cls.session.query(column('1')).from_statement(text('SELECT 1')).all()

class ReportManager(BaseManager):

    @classmethod
    def get_most_requested_ingredient(cls)-> dict:
        result = cls.session.query(Ingredient.name, func.count(OrderDetail.ingredient_id).label('total')).join(OrderDetail).group_by(Ingredient).order_by(desc('total')).first()

        return {"ingredient": result.name, "total":result.total} if result is not None else {}

    @classmethod
    def get_month_with_most_revenue(cls)-> dict:
        result = cls.session.query( extract('month', Order.date).label('month'), extract('year', Order.date).label('year'), func.sum(Order.total_price).label('total_sales')).group_by('month').order_by(desc('total_sales')).first()

        return {"month": result.month, "year": result.year, "total_sales": round(result.total_sales,2)} if result is not None else {}

    @classmethod
    def get_top_customers(cls)-> list:
        top_customers = []
        result = cls.session.query(Order.client_name, func.sum(Order.total_price).label('total')).group_by(Order.client_name).order_by(desc('total')).limit(3).all()
        for customer in result:
            top_customers.append(
                {'client_name': customer[0], 'total': customer[1]})
        return top_customers if len(top_customers) > 0 else {}

    @classmethod
    def get_full_report(cls) -> dict:
        return {
            'top_customers': cls.get_top_customers(),
            'most_requested_ingredient': cls.get_most_requested_ingredient(),
            'month_with_most_revenue': cls.get_month_with_most_revenue()
        }
