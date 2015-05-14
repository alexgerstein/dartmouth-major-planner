import pytest
from dartplan.models import Term

SEASONS = ["W", "S", "X", "F"]


class TestTerm():

    def test_term_too_early(self, term):
        if term.season == "F":
            term.season = "X"
        start_term_season = SEASONS[SEASONS.index(term.season) + 1]
        start_term = Term(year=term.year, season=start_term_season)
        end_term = Term(year=term.year + 5, season="F")

        assert not term.in_range(start_term, end_term)

    def test_term_too_late(self, term):
        if term.season == "W":
            term.season = "S"
        end_term_season = SEASONS[SEASONS.index(term.season) - 1]
        end_term = Term(year=term.year, season=end_term_season)
        start_term = Term(year=term.year - 5, season="F")

        assert not term.in_range(start_term, end_term)

    def test_year_out_of_range(self, term):
        start_term = Term(year=term.year + 1, season="F")
        end_term = Term(year=term.year + 5, season="F")

        assert not term.in_range(start_term, end_term)

    def test_year_definitely_in_range(self, term):
        start_term = Term(year=term.year - 1, season="F")
        end_term = Term(year=term.year + 1, season="F")

        assert term.in_range(start_term, end_term)

    def test_term_on_start_boundary(self, term):
        start_term = Term(year=term.year, season=term.season)
        end_term = Term(year=term.year + 1, season="F")

        assert term.in_range(start_term, end_term)

    def test_term_on_end_boundary(self, term):
        start_term = Term(year=term.year - 1, season=term.season)
        end_term = Term(year=term.year, season=term.season)

        assert term.in_range(start_term, end_term)
