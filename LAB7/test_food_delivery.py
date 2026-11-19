import math

from hypothesis import given, settings, strategies as st
from food_delivery import parse_order, delivery_eta, coupon_discount

# Anything a caller might reasonably (or unreasonably) pass in.
any_input = (
    st.text()
    | st.none()
    | st.integers()
    | st.floats(allow_nan=True, allow_infinity=True)
    | st.booleans()
    | st.lists(st.text(), max_size=3)
)

# Text built from the characters the parsers actually care about, so Hypothesis
# reaches the interesting branches much more often than with plain st.text().
order_like = st.text(alphabet="pizaburge:,0123456789 -.", max_size=30)
number_like = st.text(alphabet="0123456789.-+eEinfaINFA ", max_size=12)
coupon_like = st.text(alphabet="SAVEsave0123456789-+. x", max_size=12)


# ---------------------------------------------------------------- parse_order

@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    try:
        parse_order(s)
    except Exception as e:
        assert False, f"parse_order crashed with: {e!r}"


@settings(max_examples=300)
@given(any_input | order_like)
def test_parse_order_returns_valid_order(s):
    try:
        order = parse_order(s)
    except Exception as e:
        assert False, f"parse_order crashed with: {e!r}"
    assert isinstance(order, dict)
    for name, qty in order.items():
        assert isinstance(name, str) and name.strip() != "", f"bad item name {name!r}"
        assert isinstance(qty, int) and qty > 0, f"bad quantity {qty!r} for {name!r}"


item_names = st.text(
    alphabet=st.characters(blacklist_characters=",:", blacklist_categories=("Cs",)),
    min_size=1,
).filter(lambda n: n.strip() != "")


@given(st.dictionaries(item_names, st.integers(min_value=1, max_value=99), min_size=1))
def test_parse_order_roundtrip(order):
    # A well-formed CSV must parse back into exactly the order that produced it.
    order = {name.strip(): qty for name, qty in order.items()}
    csv = ",".join(f"{name}:{qty}" for name, qty in order.items())
    assert parse_order(csv) == order


# ------------------------------------------------------------- delivery_eta

@given(st.text() | st.none())
def test_delivery_eta_no_crash(s):
    try:
        delivery_eta(s)
    except Exception as e:
        assert False, f"delivery_eta crashed with: {e!r}"


@settings(max_examples=300)
@given(any_input | number_like)
def test_delivery_eta_returns_sane_value(d):
    try:
        eta = delivery_eta(d)
    except Exception as e:
        assert False, f"delivery_eta crashed with: {e!r}"
    # Either the input is rejected (None) or we get a whole number of minutes
    # that is at least the 15 minute base time.
    assert eta is None or (isinstance(eta, int) and eta >= 15), f"bad ETA {eta!r} for {d!r}"


@given(st.floats(min_value=0, max_value=100, allow_nan=False))
def test_delivery_eta_valid_distance(d):
    assert delivery_eta(d) == int(15 + d * 4)
    assert delivery_eta(str(d)) == int(15 + d * 4)


# ---------------------------------------------------------- coupon_discount

@given(st.text() | st.none())
def test_coupon_discount_no_crash(s):
    try:
        coupon_discount(s)
    except Exception as e:
        assert False, f"coupon_discount crashed with: {e!r}"


@settings(max_examples=300)
@given(any_input | coupon_like)
def test_coupon_discount_in_range(code):
    try:
        discount = coupon_discount(code)
    except Exception as e:
        assert False, f"coupon_discount crashed with: {e!r}"
    assert isinstance(discount, int) and 0 <= discount <= 100, \
        f"discount {discount!r} out of range for {code!r}"


@given(st.integers(min_value=1, max_value=100), st.sampled_from(["SAVE", "save", "Save"]))
def test_coupon_discount_valid_codes(pct, prefix):
    assert coupon_discount(f"{prefix}{pct}") == pct
