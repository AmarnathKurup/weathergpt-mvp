import csv
import os
import re
from typing import Dict, Any, List, Optional
from backend.app.core.config import settings
from backend.app.schemas.location import PincodeDetails

# Fallback district centroids for Indian states/districts when specific PIN lat/lon is NA
DISTRICT_CENTROIDS = {
    "KOLKATA": (22.5726, 88.3639),
    "DELHI": (28.6139, 77.2090),
    "NEW DELHI": (28.6139, 77.2090),
    "MUMBAI": (19.0760, 72.8777),
    "BENGALURU": (12.9716, 77.5946),
    "BANGALORE": (12.9716, 77.5946),
    "CHENNAI": (13.0827, 80.2707),
    "HYDERABAD": (17.3850, 78.4867),
    "PUNE": (18.5204, 73.8567),
    "AHMEDABAD": (23.0225, 72.5714),
    "JAIPUR": (26.9124, 75.7873),
    "LUCKNOW": (26.8467, 80.9462),
    "PATNA": (25.5941, 85.1376),
    "BHOPAL": (23.2599, 77.4126),
    "GUWAHATI": (26.1445, 91.7362),
    "CHANDIGARH": (30.7333, 76.7794),
    "SRINAGAR": (34.0837, 74.7973),
    "THIRUVANANTHAPURAM": (8.5241, 76.9366),
    "BHUBANESWAR": (20.2961, 85.8245),
    "RANCHI": (23.3441, 85.3096),
    "DEHRADUN": (30.3165, 78.0322),
    "SHIMLA": (31.1048, 77.1734),
}

class PincodeService:
    def __init__(self, csv_path: str = None):
        self.csv_path = csv_path or settings.PINCODE_DATA_PATH
        self.pincode_map: Dict[str, List[PincodeDetails]] = {}
        self.loaded = False

    def load_data(self):
        if self.loaded:
            return

        target_path = self.csv_path
        if not os.path.exists(target_path):
            # Fallback path check
            alt_path = os.path.join(os.getcwd(), "pincode.csv")
            if os.path.exists(alt_path):
                target_path = alt_path
            else:
                print(f"[PincodeService] Warning: Pincode file not found at {self.csv_path}")
                self.loaded = True
                return

        print(f"[PincodeService] Indexing Pincode Dataset from {target_path}...")
        count = 0
        try:
            with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    pin = str(row.get("pincode", "")).strip()
                    if not pin or not pin.isdigit() or len(pin) != 6:
                        continue

                    lat_raw = str(row.get("latitude", "")).strip()
                    lon_raw = str(row.get("longitude", "")).strip()

                    lat = float(lat_raw) if lat_raw and lat_raw.upper() != "NA" else None
                    lon = float(lon_raw) if lon_raw and lon_raw.upper() != "NA" else None

                    district = str(row.get("district", "")).strip()
                    state = str(row.get("statename", "")).strip()

                    # Fallback to district centroids if lat/lon missing in official record
                    if (lat is None or lon is None) and district.upper() in DISTRICT_CENTROIDS:
                        c_lat, c_lon = DISTRICT_CENTROIDS[district.upper()]
                        lat = lat or c_lat
                        lon = lon or c_lon

                    item = PincodeDetails(
                        pincode=pin,
                        office_name=str(row.get("officename", "")).strip(),
                        district=district,
                        state=state,
                        latitude=lat,
                        longitude=lon,
                        circle=str(row.get("circlename", "")).strip(),
                        region=str(row.get("regionname", "")).strip()
                    )

                    if pin not in self.pincode_map:
                        self.pincode_map[pin] = []
                    self.pincode_map[pin].append(item)
                    count += 1
            print(f"[PincodeService] Successfully indexed {len(self.pincode_map)} unique PIN codes ({count} post offices).")
        except Exception as e:
            print(f"[PincodeService] Error loading pincode csv: {e}")

        self.loaded = True

    def get_by_pincode(self, pin: str) -> Optional[PincodeDetails]:
        if not self.loaded:
            self.load_data()

        pin_clean = str(pin).strip()
        matches = self.pincode_map.get(pin_clean)
        if matches:
            # Pick first with valid lat/lon, or first overall
            for m in matches:
                if m.latitude is not None and m.longitude is not None:
                    return m
            # If lat/lon still missing, return first with fallback coordinates
            first = matches[0]
            first.latitude = first.latitude or 20.5937
            first.longitude = first.longitude or 78.9629
            return first
        return None

    def search_by_name(self, query: str) -> List[PincodeDetails]:
        if not self.loaded:
            self.load_data()

        q_clean = query.strip().upper()
        results = []
        for pin, items in self.pincode_map.items():
            for item in items:
                if q_clean in item.office_name.upper() or q_clean in item.district.upper() or q_clean in item.state.upper():
                    results.append(item)
                    if len(results) >= 10:
                        return results
        return results

pincode_service = PincodeService()
