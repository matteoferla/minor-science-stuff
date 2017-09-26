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

import argparse, re, urllib.request, json
from pprint import PrettyPrinter
from collections import Counter, defaultdict

pp = PrettyPrinter()


#import csv, os, re
#from Bio import SeqIO

def main(infile, outfile):
    """
    Gets a PFAM tree and makes it legible for humans by sub the ids for the gene names (via uniprot db)
    NB. a temp.json file contains the sub values.
    :param infile: tree from pfam
    :param outfile: better tree
    """
    ##############################
    # read tree and parse
    tree=open(infile).read()
    genes=[re.search('(.*)_(.*)\/(.*)\:',x).groups() for x in tree.replace('(',',').replace(')',',').split(',') if x and x.find('/') != -1]

    print(genes)
    genedex={}
    ##############################
    # get each gene from the web
    for (id,species,rng) in genes:
        try:
            try:
                seq = urllib.request.urlopen('http://www.uniprot.org/uniprot/{0}.fasta'.format(id)).read().decode('utf-8')
            except urllib.error.HTTPError:
                seq = urllib.request.urlopen('http://www.uniprot.org/uniprot/{0}_{1}.fasta'.format(id,species)).read().decode(
                    'utf-8')
                id=id+'_'+species
            header=seq.split('\n')[0]
            '>tr|Q97J65|Q97J65_CLOAB Pyruvate-formate lyase-activating enzyme OS=Clostridium acetobutylicum (strain ATCC 824 / DSM 792 / JCM 1419 / LMG 5710 / VKM B-1787) GN=CA_C1421 PE=4 SV=1'
            new_name=re.match('>.*? (.*) OS\=',header).group(1).replace(' ','_').replace('-','_')
            genedex[id]=re.sub('\W','_',new_name)
        except Exception as err:
            # exceptions are lazily nonfatal
            print('*'*20)
            print('http://www.uniprot.org/uniprot/{0}.fasta'.format(id))
            print(str(err))
            genedex[id]='id:{id}_{species}'.format(id=id,species=species)
    open('temp.json', 'w').write(json.dumps(genedex))
    #genedex = json.load(open('temp.json', 'r'))
    ##############################
    # solve duplicate name issue
    gc = Counter(genedex.values())
    gci = defaultdict(int)
    for id in genedex.keys():
        if gc[genedex[id]] >1:
            gci[genedex[id]]=gci[genedex[id]]+1
            genedex[id]=genedex[id]+'-'+str(gci[genedex[id]])
            print(id,genedex[id])
    ##############################
    # change tree and write
    for id in genedex.keys():
        tree=re.sub('{}_\w+\/\d+\-\d+'.format(id),genedex[id],tree)
        tree = re.sub('{}\/\d+\-\d+'.format(id), genedex[id], tree)
    open(outfile,'w').write(tree)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("input", help="the input file")
    parser.add_argument("output", help="the output file")
    parser.add_argument('--version', action='version', version=__version__)
    args = parser.parse_args()
    main(args.input, args.output)