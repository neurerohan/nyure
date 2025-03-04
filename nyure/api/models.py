from django.db import models
from django.utils import timezone

class Vegetable(models.Model):
    name = models.CharField(max_length=150)  # Increased length to accommodate longer names
    name_nepali = models.CharField(max_length=150)  # Storing the original Nepali name
    unit = models.CharField(max_length=30)  # Increased for units in Nepali
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    avg_price = models.DecimalField(max_digits=10, decimal_places=2)
    scrape_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name_nepali} - {self.scrape_date}"
    
    class Meta:
        unique_together = ('name_nepali', 'scrape_date')
        ordering = ['-scrape_date', 'name_nepali']