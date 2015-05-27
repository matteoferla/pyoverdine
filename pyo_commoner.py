__author__ = 'Matteo'
__doc__='''This script finds the common strains (keys of geneball dictionary of SeqRecord objects).'''


import csv
import pickle
from Bio import SeqIO
from Bio import Entrez
megageneball={}
strains={}
queries=['fpvA1','fpvA2','fpvA3','fpvI','fpvR']
for q in queries:
    file=open(q+'_pickled.dat','rb')
    megageneball[q]=pickle.load(file)
    strains[q]=megageneball[q].keys()
common= set(list(strains['fpvA1'])+list(strains['fpvA2'])+list(strains['fpvA3'])) & set(strains['fpvR'])& set(strains['fpvI'])
f=open('common.txt','w')
f.write('\n'.join(list(common)))
f.close

###PART A. download all matches.
###PART B. gene clean-up. delete small matches. delete low similarity matches
###PART C. gene numbers per strain
###PART D. fasta of common.