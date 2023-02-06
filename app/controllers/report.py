from ..repositories.managers import ReportFacade, ReportManager
from .base import BaseController

class ReportController(BaseController):
    manager = ReportManager

    @classmethod
    def get_report(cls):
        return ReportFacade(ReportManager).get_full_report(), None

