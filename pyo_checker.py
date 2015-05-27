__author__ = 'Matteo'
__doc__='''This script checks what's the similarity of the SeqRecords within each strain and other tests.'''
####Incomplete as non-essential.


import csv
import pickle
import numpy
import scipy.io as sio
from Bio import SeqIO
from Bio import Entrez

length_cutoff=20  #percent
id_cutoff=float(20)      #percent

queries=['fpvA1','fpvA2','fpvA3','fpvI','fpvR']
ref =open('common.txt','r')
constr=list(ref.readlines())

for query in queries:
    file=open(query+'_pickled.dat','rb')
    geneball=pickle.load(file)
    fl=open(query+"output_l.txt", "w")
    fi=open(query+"output_i.txt", "w")
    for strain in constr:
        #good=0
        #1query	2targets	3Id %	4??	5length	6???	7??	8Qs	9Qe	10Ss	S11e	12e	13bit
        length=[(int(gene.blast[9])-int(gene.blast[10]))/(int(gene.blast[7])-int(gene.blast[8]))*100 for gene in geneball[strain]]
        id=[(float(gene.blast[2])) for gene in geneball[strain]]
        #if (length > length_cutoff) and (id > id_cutoff):
        #    good+=1
        fl.write(strain+'\t'+'\t'.join(length)+'\n')
        fi.write(strain+'\t'+'\t'.join(id)+'\n')






###PART B. gene clean-up. delete small matches. delete low similarity matches


