import requests
from bs4 import BeautifulSoup
from decimal import Decimal
from django.utils import timezone
import logging
import re

logger = logging.getLogger(__name__)


def scrape_kalimati_market():
    """
    Scrapes vegetable prices from kalimatimarket.gov.np
    Returns a list of dictionaries containing the scraped data
    """
    url = "https://kalimatimarket.gov.np"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4XX/5XX responses

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing vegetable prices - based on the provided HTML structure
        price_table = soup.find('table', id='commodityDailyPrice')

        if not price_table:
            logger.error("Price table not found on the website")
            return []

        vegetables = []

        # Skip the header row
        rows = price_table.find('tbody').find_all('tr')

        for row in rows:
            cols = row.find_all('td')

            if len(cols) >= 4:  # Ensure we have all required columns
                try:
                    # Extract the name and unit from the first column
                    name_with_unit = cols[0].text.strip()
                    # Split name and unit - unit is in parentheses
                    name_parts = name_with_unit.split('(')
                    name_nepali = name_parts[0].strip()

                    # Extract unit from parentheses and remove closing parenthesis
                    unit = '(' + name_parts[1] if len(name_parts) > 1 else '(N/A)'
                    unit = unit.strip()

                    # Extract prices
                    # Remove 'रू ' prefix and convert to Decimal
                    min_price_text = cols[1].text.strip().replace('रू ', '')
                    max_price_text = cols[2].text.strip().replace('रू ', '')
                    avg_price_text = cols[3].text.strip().replace('रू ', '')

                    # Clean up price text by removing Nepali numerals and making sure it's valid Decimal format
                    # Replace Nepali digits with empty string and handle any special characters
                    min_price_text = re.sub(r'[^\d.]', '', min_price_text)
                    max_price_text = re.sub(r'[^\d.]', '', max_price_text)
                    avg_price_text = re.sub(r'[^\d.]', '', avg_price_text)

                    # Convert to Decimal, handling empty strings
                    min_price = Decimal(min_price_text) if min_price_text else Decimal('0')
                    max_price = Decimal(max_price_text) if max_price_text else Decimal('0')
                    avg_price = Decimal(avg_price_text) if avg_price_text else Decimal('0')

                    # Create a simplified English name based on Nepali name
                    # This is a simplification - ideally you would have a mapping dictionary
                    # For example: "गोलभेडा ठूलो(नेपाली)" -> "Tomato (Large Nepali)"
                    name = name_nepali  # For now, just use the Nepali name

                    vegetable = {
                        'name': name,
                        'name_nepali': name_nepali,
                        'unit': unit,
                        'min_price': min_price,
                        'max_price': max_price,
                        'avg_price': avg_price,
                        'scrape_date': timezone.now().date(),
                    }

                    vegetables.append(vegetable)
                except (ValueError, IndexError) as e:
                    logger.error(f"Error parsing row: {e}")
                    continue

        logger.info(f"Successfully scraped {len(vegetables)} vegetables")
        return vegetables

    except requests.RequestException as e:
        logger.error(f"Error fetching data from kalimatimarket.gov.np: {e}")
        return []