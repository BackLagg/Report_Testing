from rest_framework import viewsets
from .models import Indicator, MonthlyFormHeader, MonthlyFormLine, Company
from .serializers import IndicatorSerializer, MonthlyFormHeaderSerializer, MonthlyFormLineSerializer, CompanySerializer
import xlsxwriter
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
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

    # Запрос данных из представления full_report
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT * FROM full_report
                WHERE start_date >= %s AND end_date <= %s
                ORDER BY company_name, article_order
            """, [start_date, end_date])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

    # Проверка данных
    if not rows:
        return HttpResponse("No data found for the given date range.", status=404)

    # Генерация Excel файла
    output = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    output['Content-Disposition'] = 'attachment; filename=report.xlsx'
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # Настройки форматов
    bold_format = workbook.add_format({'bold': True})
    merge_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
        'text_wrap': True
    })
    border_format = workbook.add_format({'border': 1})
    total_format = workbook.add_format({'bold': True, 'border': 1})
    vertical_text_format = workbook.add_format({ 'bold': True, 'border': 1, 'align': 'center', 'valign': 'vcenter'})
    vertical_text_format.set_rotation(90)

    # Ширина колонок
    worksheet.set_column(0, 0, 30)  # Company
    worksheet.set_column(1, 1, 15)  # Start Date
    worksheet.set_column(2, 2, 15)  # End Date

    # Заголовок с датами
    worksheet.merge_range('A1:G1', f'Период : с {start_date} по {end_date}', merge_format)

    # Определение заголовков статей
    articles = {}
    for data in rows:
        article_name = data[4]
        if article_name not in articles:
            articles[article_name] = len(articles)

    article_start_col = 1
    for article, col_idx in articles.items():
        col = article_start_col + col_idx * 3
        worksheet.merge_range(1, col, 1, col + 2, article, merge_format)
        worksheet.set_column(col, col + 2, 10)  # Установка узкой ширины для колонок статей
        worksheet.write(2, col, 'Всего', vertical_text_format)
        worksheet.write(2, col + 1, 'Распределение', vertical_text_format)
        worksheet.write(2, col + 2, 'Целевое', vertical_text_format)


    # Заполнение данных
    row = 3
    company_totals = {article: [0, 0, 0] for article in articles}

    company_data = {}
    for data in rows:
        company_name = data[0]
        if company_name not in company_data:
            company_data[company_name] = {article: [0, 0, 0] for article in articles}

        article_name = data[4]
        distribution_value = data[6]
        target_value = data[7]
        total_value = distribution_value + target_value
        company_data[company_name][article_name][0] += total_value  # Всего
        company_data[company_name][article_name][1] += distribution_value  # Распределение
        company_data[company_name][article_name][2] += target_value  # Целевое

    for company_name, articles_data in company_data.items():
        worksheet.write(row, 0, company_name, border_format)
        for article, col_idx in articles.items():
            col = article_start_col + col_idx * 3
            worksheet.write(row, col, articles_data[article][0], border_format)
            worksheet.write(row, col + 1, articles_data[article][1], border_format)
            worksheet.write(row, col + 2, articles_data[article][2], border_format)

            # Добавление значений к итогам
            company_totals[article][0] += articles_data[article][0]
            company_totals[article][1] += articles_data[article][1]
            company_totals[article][2] += articles_data[article][2]
        row += 1

    # Добавление строки "Итого"
    worksheet.write(row, 0, 'Итого', total_format)
    for article, col_idx in articles.items():
        col = article_start_col + col_idx * 3
        worksheet.write(row, col, company_totals[article][0], total_format)
        worksheet.write(row, col + 1, company_totals[article][1], total_format)
        worksheet.write(row, col + 2, company_totals[article][2], total_format)

    workbook.close()
    return output
def report_page(request):
    return render(request, 'report.html')