# models.py
from django.db import models

class Expense(models.Model):
    name = models.CharField(max_length=100)
    reason = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return f"{self.name} - ₹{self.amount}"
