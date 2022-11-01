#!/usr/bin/env python

"""Creates a list of (almost) all german words from the openthesaurus data."""

__author__ = 'Dr. Rudolf Jagdhuber'
__status__ = 'Development'

import io
import re
import requests
import zipfile
import pandas as pd

THESAURUS = 'https://www.openthesaurus.de/export/OpenThesaurus-Textversion.zip'

# Read the file and split everything by ';' (words), '\n' (logical groups),
# ' ' (splits multi term expressions eg 'etwas verstehen', but also creates
# duplicates). [161:] removes the header of the file
words = (
    zipfile.ZipFile(io.BytesIO(requests.get(THESAURUS).content))
    .read('openthesaurus.txt')
    .decode('utf-8')
    .replace('\n', ';')  # A newline can also seperate words
    .replace(' ', ';')   # Split multi term expressions, like 'etwas verstehen'
    .split(';')          # Do the word split
    [161:]               # Remove the header of the file
)

# Remove annotations in parentheses. Eg '(fachspr.' or 'technisch)'
words = [x for x in words if not (x.startswith('(') or x.endswith(')'))]

# Remove ellipsis words like 'Konzessions...'
words = [x for x in words if not x.endswith('...')]

# Make all upercase and remove words with special characters. Eg 'O-Ton'
words = [x.upper() for x in words]
words = [x for x in words if re.match('^[A-ZÄÜÖ]+$', x)]

# Remove duplicates by converting to a set, but keep list for sorting
words = list(set(words))

# Find all words of length 5 and sort them
words5 = [x for x in words if len(x) == 5]
words5.sort()

# Save them as simple comma seperated list
with open('data/len5.txt', 'w', encoding='UTF-8') as f:
    f.write(','.join(words5))

# store them with index as CSV
words5i = [f'{a},{b}' for a, b in zip(list(range(1, len(words5) + 1)), words5)]
with open('data/len5db.csv', 'w', encoding='UTF-8') as f:
    f.write('\n'.join(words5i))
