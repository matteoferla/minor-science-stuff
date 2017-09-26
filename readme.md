## heteroduplex_resolvatase.py
See [in vivo shuffling blog post](http://blog.matteoferla.com/2017/07/in-vivo-shuffling-via-heteroduplex.html)

## fraction_coding.py
A brute force calculator to determine what is the probability a mutation is coding. The maths is simple, but my calculations were being questioned so I did it the dumb way.
I kept it simple and brutally mashed the numbers: 58% of nucleotide mutations are amino acid mutations if all mutations are equal.

## pfam_beautifier.py
Accepts a nhx tree downloaded from PFAM (tab=5) for a domain and converts the gene ids to names using Uniprot.
