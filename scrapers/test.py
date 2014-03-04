from scrape_medians import convert_median_to_float
from scrape_functions import Timetable
from app.models import Term

assert convert_median_to_float('A') == 4.00
assert convert_median_to_float('A/A-') == 3.835
assert convert_median_to_float('A-') == 3.67
assert convert_median_to_float('A-/B+') == 3.5
assert convert_median_to_float('B+') == 3.33
assert convert_median_to_float('B+/B') == 3.165


timetable_globals = Timetable()

fall = Term.query.filter_by(season = "F", year = "2013").first()
winter = Term.query.filter_by(season = "W", year = "2014").first()

old_term = Term.query.filter_by(season = timetable_globals.ARBITRARY_SEASON, year = timetable_globals.ARBITRARY_OLD_YEAR).first()

assert winter.in_range(old_term, winter)
