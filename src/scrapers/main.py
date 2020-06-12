import logging
from argparse import ArgumentParser
from functools import reduce

from models import InitiativeGroup, FeatureType
from platformen import NLvoorElkaar, WijAmsterdam, CoronaHelpersScraper, Maasburen, PuurPapendrecht, NijmegenOost
# HeldNodig, MensenDieWillenHelpen, Zorgheldenauto
from tools import Geocoder

logging.basicConfig(level=logging.DEBUG)

parser = ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", help="show this help message and exit", action="store_true")
parser.add_argument("-l", "--limit", help="LIM is the amount of items each scraper scrapes.", type=int, metavar="LIM")
parser.add_argument("-g", "--group=SIDE", choices=[InitiativeGroup.SUPPLY, InitiativeGroup.DEMAND],
                    help="Constrain supporting scrapers to only one SIDE: 'supply' or 'demand'",
                    type=str, dest="group")
parser.add_argument("-gc", "--geocoder=city", help="Enables the geocoder on city level",
                    action="store_const", const=FeatureType.CITY, dest="geocoder")
parser.add_argument("-gs", "--geocoder=settlement", help="Enables the geocoder on settlement level",
                    action="store_const", const=FeatureType.SETTLEMENT, dest="geocoder")
parser.add_argument("-ga", "--geocoder=address", help="Enables the geocoder on address level",
                    action="store_const", const=FeatureType.ADDRESS, dest="geocoder")
parser.add_argument("-s", "--scrapers", help="specifies specific scrapers to run", action="append", nargs="+", type=str)

# HeldNodig().scrape()
# MensenDieWillenHelpen().scrape()
# Zorgheldenauto().scrape()
scrapers = [
    NLvoorElkaar(),
    WijAmsterdam(),
    CoronaHelpersScraper(),
    PuurPapendrecht(),
    NijmegenOost(),
    Maasburen()]


def docs():
    parser.print_help()
    print('')
    print('If no arguments given, runs all scrapers')
    print('Use one or more codes as arguments to specify the scrapers to run:')
    print('{: <16}{}'.format("Code", "Name"))
    print('{: <16}{}'.format("____", "____"))
    for s in scrapers:
        print('{: <16}{}'.format(s.code, s.name))


arguments = parser.parse_args()

if arguments.help:
    docs()
else:
    run_scrapers = None
    if arguments.scrapers:
        print(f'Running {len(arguments.scrapers)} scrapers. Use --help to see all individual scrapers')
        run_scrapers = reduce(lambda a, b: a + b, arguments.scrapers)

        for scraper in scrapers:
            if arguments.limit:
                scraper.limit = arguments.limit
            if arguments.group:
                scraper.set_group(arguments.group)

            # preferably each scraper runs in it's own thread.
            if scraper.code in run_scrapers:
                scraper.scrape()

    # Try to create geo location for items
    if arguments.geocoder:
        print(f'Running geocoder. Use --help to see geocoder instructions')
        Geocoder().batch(arguments.geocoder)

    # The script can now be run without parameters which will do nothing. We need to tell the user this.
    if not arguments.scrapers and not arguments.geocoder:
        print(f'Nothing to do. Use --help to see detailed instructions')
