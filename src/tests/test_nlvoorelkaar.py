import re
from unittest import TestCase

import pytest

from models import InitiativeImport
from platformen.nlvoorelkaar import NLvoorElkaarSource, NLvoorElkaar


@pytest.mark.skip(reason="Test methods for debugging specific items")
class TestNLvoorElkaarPlatformSource(TestCase):
    def test_missing_plaats(self):
        scraper = NLvoorElkaar()
        item = scraper._sources[0].complete(InitiativeImport(
            source_id=179582,
            source_uri="https://www.nlvoorelkaar.nl/hulpaanbod/179582"
        ))

    def test_alternative_place_regex(self):
        text = " Deze persoon staat ingeschreven op Amstelveenvoorelkaar"
        match = re.search(r"([a-zA-Z0-9]+)voorelkaar", text)
        g = match.group(1)
        assert match is not None
