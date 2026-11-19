# L6_L7_20_food_delivery — Food Delivery

Lab 7: Fuzz Testing

## Files

| File | Description |
|------|-------------|
| `food_delivery.py` | Fixed and hardened version of the buggy application |
| `test_food_delivery.py` | Hypothesis fuzz / property-based tests |
| `PES2UG24CS084_LAB7_FuzzTesting_Screenshots.pdf` | Screenshots for Steps 2, 4, 5 and 6 |
| `screenshots/` | The individual screenshots |

## Running

```
pip install hypothesis pytest
python food_delivery.py
python -m pytest test_food_delivery.py
```

## Bugs found by fuzzing and how they were fixed

| Function | Failing inputs (found by Hypothesis) | Fix |
|----------|--------------------------------------|-----|
| `parse_order` | `None` (AttributeError), `''` / `'burger'` (no `:`, ValueError), `':'` / `'pizza:x'` (int() ValueError); also accepted `0`, negative and huge quantities, empty names, and duplicate items overwrote each other | Non-strings return `{}`; each item must be `name:qty` with a non-empty name and a whole number from 1 to 100; any malformed item rejects the order (`{}`); blank entries (e.g. trailing comma) are skipped; duplicates are summed |
| `delivery_eta` | `None` (TypeError), `''` / `'abc'` (ValueError), `'inf'` (OverflowError), `'nan'` (ValueError); negative distances gave an ETA below the 15 min base | Only `str`/`int`/`float` accepted (not `bool`); value must be finite and between 0 and 100 km, otherwise `None` |
| `coupon_discount` | `None` (AttributeError), `''` / `'WELCOME'` (IndexError), `'SAVEabc'` (ValueError); `'SAVE-20'` and `'SAVE999'` gave negative or >100% discounts | Code must be exactly `SAVE` + 1–100 (case-insensitive, ASCII only, surrounding spaces allowed); anything else returns 0 |
