import pytest
from backend.app.location.pincode_service import pincode_service

def test_pincode_indexing():
    pincode_service.load_data()
    assert pincode_service.loaded is True
    # Test valid Indian PIN lookup (e.g. Kolkata 700001 or Delhi 110001)
    res = pincode_service.get_by_pincode("700001")
    assert res is not None
    assert res.pincode == "700001"
    assert res.state is not None

def test_pincode_search_name():
    results = pincode_service.search_by_name("Kolkata")
    assert len(results) > 0
