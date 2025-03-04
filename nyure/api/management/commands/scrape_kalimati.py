from django.core.management.base import BaseCommand
from api.models import Vegetable
from api.scraper import scrape_kalimati_market
from django.utils import timezone
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Scrapes vegetable prices from kalimatimarket.gov.np'
    
    def handle(self, *args, **options):
        today = timezone.now().date()
        
        # Check if we already scraped today
        if Vegetable.objects.filter(scrape_date=today).exists():
            self.stdout.write(self.style.SUCCESS(f"Already scraped data for today ({today})"))
            return
        
        # Perform scraping
        vegetables_data = scrape_kalimati_market()
        
        if not vegetables_data:
            self.stdout.write(self.style.ERROR("Failed to scrape data or no data found"))
            return
        
        # Save the scraped data
        created_count = 0
        for veg_data in vegetables_data:
            try:
                Vegetable.objects.create(**veg_data)
                created_count += 1
            except IntegrityError:
                # Skip duplicates
                continue
            except Exception as e:
                logger.error(f"Error saving vegetable data: {e}")
        
        self.stdout.write(self.style.SUCCESS(f"Successfully scraped and saved {created_count} vegetables"))