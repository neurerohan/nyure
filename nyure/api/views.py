from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from .models import Vegetable
from .serializers import VegetableSerializer
from .scraper import scrape_kalimati_market
from django.utils import timezone
from django.db import IntegrityError
import logging
from django.http import JsonResponse
from django.core.management import call_command
from rest_framework.decorators import api_view, permission_classes

logger = logging.getLogger(__name__)

class VegetableViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows vegetables to be viewed.
    """
    queryset = Vegetable.objects.all()
    serializer_class = VegetableSerializer
    
    def get_queryset(self):
        queryset = Vegetable.objects.all()
        
        # Filter by date if provided
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(scrape_date=date)
        
        # Filter by name if provided
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        # Get latest prices if specified
        latest = self.request.query_params.get('latest')
        if latest and latest.lower() == 'true':
            latest_date = Vegetable.objects.order_by('-scrape_date').first()
            if latest_date:
                queryset = queryset.filter(scrape_date=latest_date.scrape_date)
        
        return queryset

 """
    Triggers the scraping management command via a GET request.
    """
@api_view(['GET'])
@permission_classes([IsAdminUser])  # You can adjust permission if needed
def trigger_scraping(request):

    try:
        call_command('scrape_kalimati')
        return JsonResponse({"message": "Scraping triggered successfully!"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@api_view(['POST'])
@permission_classes([IsAdminUser])
def trigger_scrape(request):
    """
    Trigger the scraping process manually.
    Only accessible to admin users.
    """
    today = timezone.now().date()
    
    # Check if we already scraped today
    if Vegetable.objects.filter(scrape_date=today).exists():
        return Response(
            {"message": f"Already scraped data for today ({today})"},
            status=status.HTTP_200_OK
        )
    
    # Perform scraping
    vegetables_data = scrape_kalimati_market()
    
    if not vegetables_data:
        return Response(
            {"error": "Failed to scrape data or no data found"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
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
    
    return Response(
        {"message": f"Successfully scraped and saved {created_count} vegetables"},
        status=status.HTTP_201_CREATED
    )
