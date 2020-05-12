#!/bin/bash
alembic upgrade head
python scrapers/main.py --help