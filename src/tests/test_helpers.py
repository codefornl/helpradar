import random
from datetime import date
from unittest import TestCase

from platformen.mijnbuurtje import MijnBuurtjeSource


class TestHelpers(TestCase):
    def test_format_group_demand(self):
        assert MijnBuurtjeSource.format_group('Hulpvraag van klaas') == 'demand'

    def test_format_group_supply(self):
        assert MijnBuurtjeSource.format_group('Iets anders') == 'supply'

    def test_format_organizer_none(self):
        assert MijnBuurtjeSource.format_organizer(None) is None

    def test_format_organizer_empty(self):
        assert MijnBuurtjeSource.format_organizer('') is None

    def test_format_organizer_simple(self):
        assert MijnBuurtjeSource.format_organizer('blub') == 'blub'

    def test_format_organizer_dash(self):
        assert MijnBuurtjeSource.format_organizer('eerste-deel') == 'eerste'

    def test_format_organizer_space(self):
        assert MijnBuurtjeSource.format_organizer('eerste deel') == 'eerste'

    def test_format_date_should_raise_on_segment_length(self):
        for date in ["18", "18 mei", "18 mei 2020 16:00"]:
            with self.subTest("Error date", date=date):
                with self.assertRaises(ValueError):
                    MijnBuurtjeSource.format_date(date)

    def test_format_months(self):
        for i, month in enumerate(["JANUARI",
                     "Februari",
                     "maart",
                     "APRil",
                     "Mei ",
                     "  juni",
                     "  Juli  ",
                     "augustus    ",
                     "September",
                     "Oktober",
                     "november",
                     "december"]):
            with self.subTest("Date", month=month):
                day = random.randint(1, 28)
                year = 2000 + random.randint(20, 30)
                actual = MijnBuurtjeSource.format_date(f"{day} {month} {year}")
                assert date(year, i + 1, day) == actual
