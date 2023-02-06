from ..repositories.managers import ReportManager
from .base import BaseController

class ReportController(BaseController):
    manager = ReportManager

    @classmethod
    def get_report(cls):
        return ReportManager.get_full_report(), None

