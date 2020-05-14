from unittest import TestCase

import pytest
from bs4 import BeautifulSoup

from models import InitiativeImport
from platformen.nlvoorelkaar import NLvoorElkaarSource, NLvoorElkaar


class TestNLvoorElkaarPlatformSource(TestCase):

    @pytest.mark.skip(reason="Test methods for debugging specific items")
    def test_missing_plaats(self):
        scraper = NLvoorElkaar()
        item = scraper._sources[0].complete(InitiativeImport(
            source_id=179582,
            source_uri="https://www.nlvoorelkaar.nl/hulpaanbod/179582"
        ))

    def test_alternative_place_regex(self):
        html = '<ul class="list list--checked">'\
               '<li>Het hulpaanbod van Joeri is bekeken door de helpdesk</li>'\
               '<li> Deze persoon staat ingeschreven op Amstelveenvoorelkaar</li>'\
               '</ul>"'
        soup = BeautifulSoup(html, 'html.parser')

        initiative = InitiativeImport()
        NLvoorElkaarSource.try_alternative_place(soup, initiative)

        assert initiative.location == "Amstelveen"
