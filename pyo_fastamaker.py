__author__ = 'Matteo'
__doc__='''This script make a fasta and a map file.'''


import csv
import pickle
from Bio import SeqIO
from Bio import Entrez

N="\n"
T="\t"

queries=['fpvA','fpvI','fpvR']
q=queries[1]

comfile=open('common.txt','r')
comstrains=[a.rstrip() for a in comfile.readlines()]
print(len(comstrains))

mapfile=open(q+'_map.txt','w')

file=open(q+'_pickled.dat','rb')
geneball=pickle.load(file)
#minigeneball=[geneball[c][0] for c in comstrains]
minigeneball=[]
for c in comstrains:
    gene=geneball[c][0]
    mapfile.write(T.join([c,gene.id,gene.description,gene.annotations['gi'],N]))
    gene.id=c
    gene.description=''
    minigeneball.append(gene)
SeqIO.write(minigeneball, q+".faa", "fasta")

file.close()
mapfile.close()


###PART A. download all matches.
###PART B. gene clean-up. delete small matches. delete low similarity matches
###PART C. gene numbers per strain
###PART D. fasta of common.