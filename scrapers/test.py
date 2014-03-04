from scrape_medians import convert_median_to_float

assert convert_median_to_float('A') == 4.00
assert convert_median_to_float('A/A-') == 3.835
assert convert_median_to_float('A-') == 3.67
assert convert_median_to_float('A-/B+') == 3.5
assert convert_median_to_float('B+') == 3.33
assert convert_median_to_float('B+/B') == 3.165
