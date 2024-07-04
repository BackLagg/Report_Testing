from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import IndicatorViewSet, MonthlyFormHeaderViewSet, MonthlyFormLineViewSet
from .views import generate_report
from .views import report_page

router = DefaultRouter()
router.register(r'indicators', IndicatorViewSet)
router.register(r'monthly_form_headers', MonthlyFormHeaderViewSet)
router.register(r'monthly_form_lines', MonthlyFormLineViewSet)

urlpatterns = [
    path('', report_page, name='report_page'),
    path('generate_report/', generate_report, name='generate_report'),
]
