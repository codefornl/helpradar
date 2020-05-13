"""
Created on Thu May  7 20:54:42 2020

@author: J.S. Kroodsma
"""
import re


def format_group(str0):
    if len(re.findall('Hulpvraag.*?', str0)) > 0:
        return 'demand'
    else:
        return 'supply'


def format_organizer(str0):
    if str0 is not None:
        list0 = str0.split('/')
        organizer_name = None if len(list0) == 0 else list0[len(list0) - 1]
        # get the first name of the organizer:
        if organizer_name is not None:
            organizer_name = re.sub('-', ' ', organizer_name)
            organizer_name = organizer_name.split(' ')[0]
    else:
        organizer_name = None
    return organizer_name
