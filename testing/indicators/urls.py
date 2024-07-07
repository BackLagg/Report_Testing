from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IndicatorViewSet, MonthlyFormHeaderViewSet, MonthlyFormLineViewSet, CompanyViewSet
from .views import generate_report
from .views import report_page

router = DefaultRouter()
router.register(r'indicators', IndicatorViewSet)
router.register(r'monthly_form_headers', MonthlyFormHeaderViewSet)
router.register(r'monthly_form_lines', MonthlyFormLineViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Включение маршрутов, созданных DefaultRouter
    path('report/', report_page, name='report_page'),
    path('generate_report/', generate_report, name='generate_report'),
]
