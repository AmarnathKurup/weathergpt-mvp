import re
import httpx
from typing import Optional, Tuple
from backend.app.schemas.weather import LocationInfo
from backend.app.location.pincode_service import pincode_service, DISTRICT_CENTROIDS

MAJOR_INDIAN_CITIES = {
    "KOLKATA": (22.5726, 88.3639, "Kolkata", "West Bengal", "700001"),
    "DELHI": (28.6139, 77.2090, "Delhi", "Delhi", "110001"),
    "NEW DELHI": (28.6139, 77.2090, "New Delhi", "Delhi", "110001"),
    "MUMBAI": (19.0760, 72.8777, "Mumbai", "Maharashtra", "400001"),
    "BENGALURU": (12.9716, 77.5946, "Bengaluru", "Karnataka", "560001"),
    "BANGALORE": (12.9716, 77.5946, "Bengaluru", "Karnataka", "560001"),
    "CHENNAI": (13.0827, 80.2707, "Chennai", "Tamil Nadu", "600001"),
    "HYDERABAD": (17.3850, 78.4867, "Hyderabad", "Telangana", "500001"),
    "PUNE": (18.5204, 73.8567, "Pune", "Maharashtra", "411001"),
    "AHMEDABAD": (23.0225, 72.5714, "Ahmedabad", "Gujarat", "380001"),
    "JAIPUR": (26.9124, 75.7873, "Jaipur", "Rajasthan", "302001"),
    "LUCKNOW": (26.8467, 80.9462, "Lucknow", "Uttar Pradesh", "226001"),
    "PATNA": (25.5941, 85.1376, "Patna", "Bihar", "800001"),
    "BHOPAL": (23.2599, 77.4126, "Bhopal", "Madhya Pradesh", "462001"),
    "GUWAHATI": (26.1445, 91.7362, "Guwahati", "Assam", "781001"),
    "DARJEELING": (27.0410, 88.2663, "Darjeeling", "West Bengal", "734101"),
    "SHIMLA": (31.1048, 77.1734, "Shimla", "Himachal Pradesh", "171001"),
    "SRINAGAR": (34.0837, 74.7973, "Srinagar", "Jammu and Kashmir", "190001"),
    "SILIGURI": (26.7271, 88.3953, "Siliguri", "West Bengal", "734001"),
    "VARANASI": (25.3176, 82.9739, "Varanasi", "Uttar Pradesh", "221001")
}

class LocationEngine:
    @staticmethod
    async def resolve_location(
        query: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> LocationInfo:
        # Method 1: GPS Direct Coordinates
        if lat is not None and lon is not None:
            return LocationInfo(
                name=f"Location ({lat:.2f}, {lon:.2f})",
                pincode="700001",
                district="User Area",
                state="India",
                latitude=lat,
                longitude=lon
            )

        if not query:
            # Default fallback to Kolkata (700001)
            return LocationInfo(
                name="Kolkata",
                pincode="700001",
                district="Kolkata",
                state="West Bengal",
                latitude=22.5726,
                longitude=88.3639
            )

        query_clean = query.strip()

        # Method 2: PIN Code match (6 digits)
        pin_match = re.search(r'\b\d{6}\b', query_clean)
        if pin_match:
            pin = pin_match.group(0)
            p_details = pincode_service.get_by_pincode(pin)
            if p_details:
                return LocationInfo(
                    name=f"{p_details.office_name} ({p_details.pincode})",
                    pincode=p_details.pincode,
                    district=p_details.district,
                    state=p_details.state,
                    latitude=p_details.latitude or 22.5726,
                    longitude=p_details.longitude or 88.3639
                )

        # Method 3: Major Indian City Direct Lookup
        q_upper = query_clean.upper()
        for city_key, data in MAJOR_INDIAN_CITIES.items():
            if city_key in q_upper:
                return LocationInfo(
                    name=data[2],
                    pincode=data[4],
                    district=data[2],
                    state=data[3],
                    latitude=data[0],
                    longitude=data[1]
                )

        # Search inside Pincode service by office/district/state name
        p_search = pincode_service.search_by_name(query_clean)
        if p_search:
            top = p_search[0]
            return LocationInfo(
                name=f"{top.office_name}, {top.district}",
                pincode=top.pincode,
                district=top.district,
                state=top.state,
                latitude=top.latitude or 22.5726,
                longitude=top.longitude or 88.3639
            )

        # Method 4: Open-Meteo Geocoding API Fallback
        try:
            url = f"https://geocoding-api.open-meteo.com/v1/search?name={query_clean}&count=1&language=en&format=json"
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(url)
                if res.status_code == 200:
                    results = res.json().get("results", [])
                    if results:
                        r = results[0]
                        return LocationInfo(
                            name=r.get("name", query_clean),
                            pincode="700001",
                            district=r.get("admin1", r.get("name")),
                            state=r.get("country", "India"),
                            latitude=float(r.get("latitude", 22.5726)),
                            longitude=float(r.get("longitude", 88.3639))
                        )
        except Exception:
            pass

        # Final safe default fallback
        return LocationInfo(
            name=query_clean.capitalize(),
            pincode="700001",
            district="Kolkata",
            state="West Bengal",
            latitude=22.5726,
            longitude=88.3639
        )

location_engine = LocationEngine()
