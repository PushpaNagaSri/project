# models.py
from django.db import models

class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()  # Optional, if you want a field for the reason

    def __str__(self):
        return f"{self.name} - ₹{self.amount}"
