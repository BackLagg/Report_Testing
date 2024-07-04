from rest_framework import viewsets
from .models import Indicator, MonthlyFormHeader, MonthlyFormLine
from .serializers import IndicatorSerializer, MonthlyFormHeaderSerializer, MonthlyFormLineSerializer
import xlsxwriter
from django.http import HttpResponse
from django.shortcuts import render

class IndicatorViewSet(viewsets.ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer

class MonthlyFormHeaderViewSet(viewsets.ModelViewSet):
    queryset = MonthlyFormHeader.objects.all()
    serializer_class = MonthlyFormHeaderSerializer

class MonthlyFormLineViewSet(viewsets.ModelViewSet):
    queryset = MonthlyFormLine.objects.all()
    serializer_class = MonthlyFormLineSerializer

def generate_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    headers = MonthlyFormHeader.objects.filter(start_date__gte=start_date, end_date__lte=end_date)
    lines = MonthlyFormLine.objects.filter(form_header__in=headers)

    output = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    output['Content-Disposition'] = 'attachment; filename=report.xlsx'
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    bold_format = workbook.add_format({'bold': True, 'border': 2, 'align': 'center', 'valign': 'vcenter'})
    border_format = workbook.add_format({'border': 2, 'align': 'center', 'valign': 'vcenter'})

    # Установить ширину столбцов и высоту строк
    worksheet.set_column(0, 0, 20)  # Organization
    worksheet.set_column(1, 2, 15)  # Start Date, End Date, Наименование статьи
    worksheet.set_column(3, 3, 50)
    worksheet.set_column(4, 5, 10)  # Целевое, Распределение
    row_height = 15 * 2  # В 2 раза больше обычной высоты
    for row_num in range(1, len(lines) + 2):  # +2 для заголовка и чтобы покрыть все строки
        worksheet.set_row(row_num, row_height)
    # Установить высоту строк


    # Write the headers
    worksheet.write(0, 0, 'Организация', bold_format)
    worksheet.write(0, 1, 'Начальная дата', bold_format)
    worksheet.write(0, 2, 'конечная дата', bold_format)
    worksheet.write(0, 3, 'Наименование статьи', bold_format)
    worksheet.write(0, 4, 'Целевое', bold_format)
    worksheet.write(0, 5, 'Распределение', bold_format)

    row = 1
    for header in headers:
        org_lines = lines.filter(form_header=header)
        line_count = org_lines.count()

        # Объединить ячейки для организации
        if line_count > 0:
            worksheet.merge_range(row, 0, row + line_count - 1, 0, header.organization, border_format)

        for line in org_lines:
            worksheet.write(row, 1, line.form_header.start_date.strftime('%Y-%m-%d'), border_format)
            worksheet.write(row, 2, line.form_header.end_date.strftime('%Y-%m-%d'), border_format)
            worksheet.write(row, 3, line.indicator.article_name, border_format)
            worksheet.write(row, 4, line.target_distribution_value, border_format)
            worksheet.write(row, 5, line.distribution_value, border_format)
            row += 1

    workbook.close()
    return output
def report_page(request):
    return render(request, 'report.html')