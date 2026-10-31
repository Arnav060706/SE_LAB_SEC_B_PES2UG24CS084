import pytest
from food_delivery import delivery_charge, apply_coupon, estimated_time


# delivery_charge: range check
@pytest.mark.parametrize("distance", [-1, 0, 15.5, 20])
def test_out_of_range_raises(distance):
    with pytest.raises(ValueError, match="out of delivery range"):
        delivery_charge(distance, 200, False)


# delivery_charge: order value and distance tiers, including boundaries
@pytest.mark.parametrize(
    "distance, order_value, expected",
    [
        (5, 500, 0),
        (5, 800, 0),
        (2, 200, 20),
        (3, 499, 20),
        (3.5, 200, 40),
        (8, 200, 40),
        (8.5, 200, 60),
        (15, 200, 60),
    ],
)
def test_charge_without_rain(distance, order_value, expected):
    assert delivery_charge(distance, order_value, False) == expected


# delivery_charge: rain applies on top of every tier
@pytest.mark.parametrize(
    "distance, order_value, expected",
    [
        (5, 500, 30),
        (2, 200, 50),
        (5, 200, 70),
        (10, 200, 90),
    ],
)
def test_charge_with_rain(distance, order_value, expected):
    assert delivery_charge(distance, order_value, True) == expected


# apply_coupon: no coupon and rejected coupons
@pytest.mark.parametrize("is_first_order", [True, False])
def test_no_coupon(is_first_order):
    assert apply_coupon(300, None, is_first_order) == 300

def test_invalid_coupon_raises():
    with pytest.raises(ValueError, match="invalid coupon"):
        apply_coupon(300, "FREEFOOD", True)

def test_welcome_coupon_rejected_for_repeat_customer():
    with pytest.raises(ValueError, match="coupon only for first order"):
        apply_coupon(300, "WELCOME", False)


# apply_coupon: minimum order value boundary
@pytest.mark.parametrize(
    "order_value, code, is_first_order, expected",
    [
        (199, "SAVE50", False, 199),
        (199, "WELCOME", True, 199),
        (200, "SAVE50", False, 150),
        (200, "WELCOME", True, 100),
    ],
)
def test_coupon_minimum_order(order_value, code, is_first_order, expected):
    assert apply_coupon(order_value, code, is_first_order) == expected

def test_save50_also_valid_on_first_order():
    assert apply_coupon(300, "SAVE50", True) == 250


# estimated_time: all peak hour / busy restaurant combinations
@pytest.mark.parametrize(
    "is_peak_hour, restaurant_busy, expected",
    [
        (False, False, 35),
        (True, False, 45),
        (False, True, 50),
        (True, True, 65),
    ],
)
def test_estimated_time(is_peak_hour, restaurant_busy, expected):
    assert estimated_time(5, is_peak_hour, restaurant_busy) == expected
