from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Bills', 'Bills'),
        ('Entertainment', 'Entertainment'),
        ('Health', 'Health'),
        ('Utility', 'Utility'),
        ('Other', 'Other'),
    ]


class Expense(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True) 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    date=models.DateField(auto_now_add=True)

    def __str__(self) :
        return f"{self.category} - {self.amount}"

class Income(models.Model):
    ICATEGORY_CHOICES = [
        ('Employment', 'Employment'),
        ('SideHustle', 'SideHustle'),
        ('Dividend', 'Dividend'),
        ('Others', 'Others'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.CharField(max_length=50, choices=ICATEGORY_CHOICES, default='Other')
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.description}"
    
class Budget(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()

    def __str__(self):
        return self.name