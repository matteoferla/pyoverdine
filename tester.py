__author__ = 'Matteo'
__doc__='''This script is a sandbox.'''

#interpreter change.
import csv
import pickle
from Bio import SeqIO
from Bio import Entrez

file=open('geneX_pickled.dat','rb')
gene=pickle._load(file)
print(len(gene.keys()))
