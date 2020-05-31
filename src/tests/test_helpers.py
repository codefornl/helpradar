import random
from collections import namedtuple
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
        for bad_date in ["18", "18 mei", "18 mei 2020 16:00"]:
            with self.subTest("Error date", date=bad_date):
                with self.assertRaisesRegex(ValueError, f"Expecting a three segment date, got {bad_date}."):
                    MijnBuurtjeSource.format_date(bad_date)

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

    def test_format_date_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            assert None is MijnBuurtjeSource.format_date("")

    def test_should_strip_none_if_none(self):
        assert None is MijnBuurtjeSource.strip_text(None, "test")

    def test_should_strip_none_if_no_text(self):
        Element = namedtuple('Element', 'text')
        assert None is MijnBuurtjeSource.strip_text(Element(text=None), "test")

