import pytest
from food_delivery import delivery_charge, apply_coupon, estimated_time


# delivery_charge
def test_nearby_small_order():
    assert delivery_charge(2, 200, False) == 20

def test_out_of_range_raises():
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(20, 200, False)

def test_free_delivery_for_large_order():
    assert delivery_charge(5, 500, False) == 0

def test_medium_distance_charge():
    assert delivery_charge(5, 200, False) == 40

def test_long_distance_charge():
    assert delivery_charge(10, 200, False) == 60

def test_rain_surcharge():
    assert delivery_charge(2, 200, True) == 50


# apply_coupon
def test_no_coupon():
    assert apply_coupon(300, None, False) == 300

def test_invalid_coupon_raises():
    with pytest.raises(ValueError, match="invalid coupon"):
        apply_coupon(300, "FREEFOOD", False)

def test_welcome_coupon_rejected_for_repeat_customer():
    with pytest.raises(ValueError, match="coupon only for first order"):
        apply_coupon(300, "WELCOME", False)

def test_coupon_ignored_below_minimum_order():
    assert apply_coupon(150, "SAVE50", False) == 150

def test_coupon_applied():
    assert apply_coupon(300, "SAVE50", False) == 250


# estimated_time
def test_time_peak_hour_and_busy_restaurant():
    assert estimated_time(5, True, True) == 65
