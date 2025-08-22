"""
STC (Sport- und Tennis-Club München Süd) booking system client.
Fetches court availability from the eBuSy booking system.
"""

import requests
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import re
from bs4 import BeautifulSoup


@dataclass
class TimeSlot:
    """Represents a time slot for booking."""
    start_time: str
    end_time: str
    is_available: bool
    court_id: str
    court_name: str


@dataclass
class CourtAvailability:
    """Represents court availability for a specific date."""
    date: date
    court_id: str
    court_name: str
    time_slots: List[TimeSlot]


class STCBookingClient:
    """Client for interacting with the STC eBuSy booking system."""
    
    def __init__(self):
        self.base_url = "https://siemens-tennisclub-muenchenv8.ebusy.de"
        self.session = requests.Session()
        # Set headers to mimic a browser request
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get_court_availability(self, target_date: date) -> List[CourtAvailability]:
        """
        Fetch court availability for a specific date.
        
        Args:
            target_date: The date to check availability for
            
        Returns:
            List of court availability data
        """
        # Format date as DD/MM/YYYY for the URL
        date_str = target_date.strftime("%d/%m/%Y")
        url = f"{self.base_url}/lite-module/891?currentDate={date_str}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            # Parse the HTML response
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract court availability from the table
            return self._parse_availability_table(soup, target_date)
            
        except requests.RequestException as e:
            print(f"Error fetching availability: {e}")
            return []
    
    def _parse_availability_table(self, soup: BeautifulSoup, target_date: date) -> List[CourtAvailability]:
        """Parse the availability table from the HTML response."""
        courts_availability = []
        
        # Find the main table containing the booking data
        table = soup.find('table')
        if not table:
            return courts_availability
        
        # Extract court headers (column names)
        headers = []
        header_row = table.find('tr')
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
        
        # Map court names to our internal court IDs
        court_mapping = self._get_court_mapping(headers)
        
        # Parse time slots
        time_rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in time_rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 2:
                continue
            
            # Extract time information
            time_cell = cells[0]
            time_text = time_cell.get_text(strip=True)
            
            # Parse time range (e.g., "07:00 bis 08:00")
            time_match = re.search(r'(\d{2}:\d{2})\s+bis\s+(\d{2}:\d{2})', time_text)
            if not time_match:
                continue
                
            start_time = time_match.group(1)
            end_time = time_match.group(2)
            
            # Check availability for each court
            for i, cell in enumerate(cells[1:], 1):
                if i >= len(headers):
                    break
                    
                court_name = headers[i] if i < len(headers) else f"Court_{i}"
                court_id = court_mapping.get(court_name, f"court_{i}")
                
                # Check if the slot is available (contains "Buchen" button)
                is_available = "Buchen" in cell.get_text()
                
                # Create time slot
                time_slot = TimeSlot(
                    start_time=start_time,
                    end_time=end_time,
                    is_available=is_available,
                    court_id=court_id,
                    court_name=court_name
                )
                
                # Add to or update court availability
                court_avail = next(
                    (ca for ca in courts_availability if ca.court_id == court_id), 
                    None
                )
                
                if court_avail is None:
                    court_avail = CourtAvailability(
                        date=target_date,
                        court_id=court_id,
                        court_name=court_name,
                        time_slots=[]
                    )
                    courts_availability.append(court_avail)
                
                court_avail.time_slots.append(time_slot)
        
        return courts_availability
    
    def _get_court_mapping(self, headers: List[str]) -> Dict[str, str]:
        """Map court names from the website to internal court IDs."""
        mapping = {}
        
        for i, header in enumerate(headers):
            header_lower = header.lower()
            
            # Map based on the court names we see in the website
            if "platz a" in header_lower:
                mapping[header] = "court_a"
            elif "platz 1" in header_lower:
                mapping[header] = "court_1"
            elif "platz 2" in header_lower:
                mapping[header] = "court_2"
            elif "platz 3" in header_lower:
                mapping[header] = "court_3"
            elif "platz 4" in header_lower:
                mapping[header] = "court_4"
            elif "platz 5" in header_lower:
                mapping[header] = "court_5"
            elif "platz 6" in header_lower:
                mapping[header] = "court_6"
            elif "platz 7" in header_lower:
                mapping[header] = "court_7"
            elif "platz 8" in header_lower:
                mapping[header] = "court_8"
            elif "platz 9" in header_lower:
                mapping[header] = "court_9"
            elif "platz 10" in header_lower:
                mapping[header] = "court_10"
            elif "platz 11" in header_lower:
                mapping[header] = "court_11"
            elif "platz 12" in header_lower:
                mapping[header] = "court_12"
            elif "t-platz" in header_lower:
                mapping[header] = "court_t"
            elif "platz 14" in header_lower:
                mapping[header] = "court_14"
            elif "platz 15" in header_lower:
                mapping[header] = "court_15"
            elif "platz 16" in header_lower:
                mapping[header] = "court_16"
            elif "platz 17" in header_lower:
                mapping[header] = "court_17"
            elif "platz 18" in header_lower:
                mapping[header] = "court_18"
            elif "platz 19" in header_lower:
                mapping[header] = "court_19"
            elif "platz 20" in header_lower:
                mapping[header] = "court_20"
            elif "platz 21" in header_lower:
                mapping[header] = "court_21"
            elif "platz 22" in header_lower:
                mapping[header] = "court_22"
            else:
                # Default mapping for unknown courts
                mapping[header] = f"court_{i}"
        
        return mapping
    
    def get_available_slots(self, target_date: date, start_time: str = None, end_time: str = None) -> List[TimeSlot]:
        """
        Get available time slots for a specific date and optional time range.
        
        Args:
            target_date: The date to check
            start_time: Optional start time filter (HH:MM format)
            end_time: Optional end time filter (HH:MM format)
            
        Returns:
            List of available time slots
        """
        courts_availability = self.get_court_availability(target_date)
        
        available_slots = []
        for court_avail in courts_availability:
            for slot in court_avail.time_slots:
                if not slot.is_available:
                    continue
                
                # Apply time filters if provided
                if start_time and slot.start_time < start_time:
                    continue
                if end_time and slot.end_time > end_time:
                    continue
                
                available_slots.append(slot)
        
        return available_slots


# Global instance for easy access
stc_client = STCBookingClient()
