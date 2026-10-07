# Fix 8: Decimals were silently cut down, and odd number formats were accepted

Covers glitches 4 and 5. One change to `parse_guess()` fixes both.

## Symptom
- `50.9` was accepted as `50` without telling you, but `1e2` was rejected as "not a number".
- `1_0` was read as 10 and the Arabic-Indic digit `٥` as 5.

## Root cause
- `parse_guess()` used `int(float(raw))` whenever there was a `.`, which cuts off the decimal part.
- Python's `int()` accepts underscores and any Unicode digit, which is more than a guessing game should allow.

## Fix (`logic_utils.py` → `parse_guess()`)
- Two regular expressions decide what counts as valid input:
  - `WHOLE_NUMBER = [+-]?[0-9]+`: plain ASCII digits with an optional sign. This is the only accepted format.
  - `DECIMAL_NUMBER`: anything like `50.9`, `100.0` or `.5` gets "Enter a whole number (no decimals)."
- Everything else (`1_0`, `٥`, `1e2`, `0x10`, `abc`) gets "That is not a number."
- Very long digit strings (Python won't convert 4300+ digits) are caught and get the range message
  instead of crashing.

## Tests
`test_decimal_rejected_not_truncated`, `test_trailing_dot_decimal_rejected`,
`test_python_only_number_formats_rejected`, `test_huge_number_does_not_crash`, `test_plus_sign_still_accepted`
