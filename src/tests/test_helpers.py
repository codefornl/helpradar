from unittest import TestCase

from platformen.helpers import format_group, format_organizer


class TestHelpers(TestCase):
    def test_format_group_demand(self):
        assert format_group('Hulpvraag van klaas') == 'demand'

    def test_format_group_supply(self):
        assert format_group('Iets anders') == 'supply'

    def test_format_organizer_none(self):
        assert format_organizer(None) is None

    def test_format_organizer_empty(self):
        assert format_organizer('') == ''

    def test_format_organizer_simple(self):
        assert format_organizer('blub') == 'blub'

    def test_format_organizer_composed(self):
        assert format_organizer('tic/tac/toe') == 'toe'

    def test_format_organizer_dash(self):
        assert format_organizer('eerste-deel') == 'eerste'

    def test_format_organizer_space(self):
        assert format_organizer('eerste deel') == 'eerste'
