from app.config import Settings
from app.integrations.access_control_service import AccessControlService
from app.integrations.imei_validation_service import CheckIMEIService
from app.stubs.access_control_service_stub import AccessControlServiceStub
from app.stubs.imei_validation_service_stub import CheckIMEIServiceStub


class AccessControlServiceBuilder:
    @staticmethod
    def build_service(settings: Settings):
        if "test" in settings.ACCESS_CONTROL_URL:
            return AccessControlServiceStub(settings.ACCESS_CONTROL_URL)
        else:
            return AccessControlService(settings.ACCESS_CONTROL_URL)


class CheckIMEIServiceBuilder:
    @staticmethod
    def build_service(settings: Settings):
        if "test" in settings.CHECK_IMEI_SERVICE_URL:
            return CheckIMEIServiceStub(settings.CHECK_IMEI_SERVICE_URL)
        else:
            return CheckIMEIService(settings.CHECK_IMEI_SERVICE_URL)
