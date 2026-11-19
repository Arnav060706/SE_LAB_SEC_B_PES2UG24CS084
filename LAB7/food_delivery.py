import math
import re

MAX_QTY = 100            # most of a single item one order may contain
MAX_DISTANCE_KM = 100.0  # furthest distance we deliver to
MAX_DISCOUNT = 100       # a coupon can never take off more than 100%

_QTY_RE = re.compile(r"[0-9]+")
_COUPON_RE = re.compile(r"SAVE([0-9]{1,3})")


def parse_order(items_csv):
    """Parse "name:qty,name:qty" into {name: qty}.

    Returns {} if the input is not a string or any item is malformed
    (missing/extra ':', empty name, non-numeric, zero or oversized quantity).
    Blank entries such as a trailing comma are ignored, and repeated items
    are added together instead of silently overwriting each other.
    """
    if not isinstance(items_csv, str):
        return {}

    order = {}
    for item in items_csv.split(','):
        if not item.strip():
            continue
        parts = item.split(':')
        if len(parts) != 2:
            return {}
        name, qty = parts[0].strip(), parts[1].strip()
        # ASCII digits only: int() would also accept '+3', '1_0' or non-latin digits
        if not name or not _QTY_RE.fullmatch(qty) or len(qty) > 3:
            return {}
        qty = int(qty)
        if not 1 <= qty <= MAX_QTY:
            return {}
        order[name] = order.get(name, 0) + qty
        if order[name] > MAX_QTY:
            return {}
    return order


def delivery_eta(distance_km):
    """Return the ETA in whole minutes, or None if the distance is invalid.

    Rejects non-numeric input, booleans, NaN, infinity, negative distances
    and anything beyond MAX_DISTANCE_KM.
    """
    if isinstance(distance_km, bool) or not isinstance(distance_km, (str, int, float)):
        return None
    try:
        distance = float(distance_km)
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(distance) or not 0 <= distance <= MAX_DISTANCE_KM:
        return None
    return int(15 + distance * 4)


def coupon_discount(code):
    """Return the percentage discount for a code like "SAVE50", or 0 if invalid.

    The code must be exactly "SAVE" followed by a number from 1 to 100
    (case-insensitive, surrounding spaces allowed).
    """
    if not isinstance(code, str):
        return 0
    code = code.strip()
    # Non-ASCII letters can upper-case into ASCII ('ſ'.upper() == 'S'), so reject them first
    if not code.isascii():
        return 0
    match = _COUPON_RE.fullmatch(code.upper())
    if not match:
        return 0
    discount = int(match.group(1))
    if not 1 <= discount <= MAX_DISCOUNT:
        return 0
    return discount


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter items as name:qty CSV (e.g. pizza:2,burger:1): ")
    result = parse_order(user_input)
    if result:
        print("Order:", result)
    else:
        print("Invalid order. Use name:qty pairs separated by commas, "
              f"with quantities from 1 to {MAX_QTY}.")

    print("\n==== Running delivery_eta ====")
    user_input = input("Enter distance in km (e.g. 4.5): ")
    result = delivery_eta(user_input)
    if result is not None:
        print("ETA in Minutes:", result)
    else:
        print(f"Invalid distance. Enter a number between 0 and {MAX_DISTANCE_KM:g} km.")

    print("\n==== Running coupon_discount ====")
    user_input = input("Enter a coupon code (e.g. SAVE50): ")
    result = coupon_discount(user_input)
    if result:
        print("Discount:", result)
    else:
        print("Invalid coupon code. No discount applied.")
        print("Discount:", result)


if __name__ == "__main__":
    main()
