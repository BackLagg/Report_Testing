from django.db import models
from django.contrib.auth.models import User
class Indicator(models.Model):
    id = models.AutoField(primary_key=True)
    date_valid_until = models.DateField()
    article_name = models.CharField(max_length=255)
    order = models.IntegerField()
    last_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='indicator_modified_by')
    def __str__(self):
        return self.article_name
class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    users = models.ManyToManyField(User, related_name='companies')  # Связь с пользователем
    def __str__(self):
        return self.name

class MonthlyFormHeader(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    organization = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class MonthlyFormLine(models.Model):
    id = models.AutoField(primary_key=True)
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE)
    form_header = models.ForeignKey(MonthlyFormHeader, on_delete=models.CASCADE)
    distribution_value = models.IntegerField()
    target_distribution_value = models.IntegerField()
    last_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='monthlyformline_modified_by')