
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__description__ = \
    """

NB. Written for python 3, not tested under 2.
"""
__author__ = "Matteo Ferla. [Github](https://github.com/matteoferla)"
__email__ = "matteo.ferla@gmail.com"
__date__ = ""
__license__ = "Cite me!"
__version__ = "1.0"

from pprint import PrettyPrinter
pprint = PrettyPrinter().pprint
import json

from urllib import request

####### VARIABLES ######
names='Acetobacter Azotobacter Bacillus Brevibacterium Burkholderia Campylobacter Corynebacterium Escherichia Geobacillus Lactobacillus Serratia Propionibacterium Pseudomonas Streptomyces Thermotoga'.split()
coterm='engineering'
####### MAIN ######
count=dict()
for name in names:
    count[name]=int(json.loads(request.urlopen('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={name}+{coterm}&rettype=Count&retmode=json'.format(name=name, coterm=coterm)).read().decode('utf-8'))['esearchresult']['count'])
s= [(k, count[k]) for k in sorted(count, key=count.get, reverse=True)]
pprint(s)
