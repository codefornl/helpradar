import logging
from argparse import ArgumentParser
from functools import reduce

from models import InitiativeGroup
from platformen import NLvoorElkaar, WijAmsterdam, CoronaHelpersScraper
from tools import Geocoder

logging.basicConfig(level=logging.DEBUG)

parser = ArgumentParser(add_help=False)
parser.add_argument("-h", "--help", help="show this help message and exit", action="store_true")
parser.add_argument("-l", "--limit", help="LIM is the amount of items each scraper scrapes.", type=int, metavar="LIM")
parser.add_argument("-g", "--group=SIDE", choices=[InitiativeGroup.SUPPLY, InitiativeGroup.DEMAND],
                    help="Constrain supporting scrapers to only one SIDE: 'supply' or 'demand'",
                    type=str, dest="group")
parser.add_argument("-n", "--nogeo", help="Disables the geocoder", action="store_true", dest="nogeo")
parser.add_argument("-s", "--scrapers", help="specifies specific scrapers to run", action="append", nargs="+", type=str)

# HeldNodig().scrape()
# MensenDieWillenHelpen().scrape()
# Zorgheldenauto().scrape()
# PuurPapendrecht().scrape()
# NijmegenOost().scrape()
scrapers = [NLvoorElkaar(), WijAmsterdam(), CoronaHelpersScraper()]


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
    print(f'Running {len(arguments.scrapers)} scrapers. Use --help to see all individual scrapers')
    if arguments.group:
        if arguments.group != InitiativeGroup.SUPPLY \
                and arguments.group != InitiativeGroup.DEMAND:
            print(f"Invalid group given {arguments.group}")
            exit()

    run_scrapers = None
    if arguments.scrapers:
        run_scrapers = reduce(lambda a, b: a + b, arguments.scrapers)

    for scraper in scrapers:
        if arguments.limit:
            scraper.limit = arguments.limit
        if arguments.group:
            scraper.set_group(InitiativeGroup.DEMAND if arguments.group == "demand" else InitiativeGroup.SUPPLY)

        # preferably each scraper runs in it's own thread.
        if not run_scrapers:
            scraper.scrape()
        elif scraper.code in run_scrapers:
            scraper.scrape()

    # Try to create geo location for items
    if not arguments.nogeo:
        Geocoder().geocode()
