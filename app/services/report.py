from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from .base import BaseService
from ..controllers import ReportController

report = Blueprint('report', __name__)

report_service = BaseService()


@report.route('/', methods=GET)
def get_report():
    return report_service.get_all(ReportController.get_report)