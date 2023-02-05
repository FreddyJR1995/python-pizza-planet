from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request
from .base import BaseService
from ..controllers import IngredientController

ingredient = Blueprint('ingredient', __name__)

ingredient_service = BaseService()

@ingredient.route('/', methods=POST)
def create_ingredient():
    return ingredient_service.create(IngredientController.create)

@ingredient.route('/', methods=PUT)
def update_ingredient():
    return ingredient_service.update(IngredientController.update)

@ingredient.route('/id/<_id>', methods=GET)
def get_ingredient_by_id(_id: int):
    return ingredient_service.get_by_id(_id, IngredientController.get_by_id)

@ingredient.route('/', methods=GET)
def get_ingredients():
    return ingredient_service.get_all(IngredientController.get_all)