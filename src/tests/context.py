import os
import sys

parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
scrapers_path = os.path.join(parent, "scrapers")

print(f"Adding {scrapers_path} to PATH")
sys.path.append(scrapers_path)

import platformen
