__author__ = 'Matteo'
__doc__='''This script combines the multiple pickled blast hits.'''

import csv
import pickle
from Bio import SeqIO
from Bio import Entrez
megageneball={}
minigeneball={}
strains={}
queries=['fpvA1','fpvA2','fpvA3']
for q in queries:
    file=open(q+'_pickled.dat','rb')
    geneball=pickle.load(file)
    for strain in geneball.keys():
        #megageneball.setdefault(strain, []).extend(geneball[strain])
        if not strain in minigeneball.keys():
            minigeneball[strain]=[geneball[strain][0]]
#print(len(megageneball))
file=open('fpvA_pickled.dat','wb')
pickle.dump(minigeneball,file)

###PART A. download all matches.
###PART B. gene clean-up. delete small matches. delete low similarity matches
###PART C. gene numbers per strain
###PART D. fasta of common.