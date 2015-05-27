__author__ = 'Matteo'
__doc__='''This script downloads, sorts and pickled blast hits.'''


#seqfile="sequence.gb"
query='fpvR'
hitfile=query+".csv"

import re
import csv
import pickle
import time
from Bio import SeqIO
from Bio import Entrez
from urllib.error import URLError
Entrez.email = "matteo.ferla@gmail.com"

def detol(word):
    return word.replace('Pseudomonas aeruginosa','').lstrip(' ')

def strained(pept):
    strain = detol(pept.annotations['source'])
    if not strain:
        strain = detol(pept.annotations['organism'])
    if not strain:
        x =pept.features[0].qualifiers
        if 'strain' in x.keys():
            strain = x['strain'][0]
        elif 'organism' in x.keys():
            strain = detol(x['organism'][0])
    if not strain:
        strain=None
    return strain

def mule(hits):
    gi=[]
    extra={}
    for hit in hits:
        if hit:
            ids=hit[1].split(';')
            for j in ids:
                new=re.search('\|(\d+)\|',j).group(0)[1:-1]
                gi.append(new)
                extra[new]=hit
    print('gi.s to do: '+str(len(gi)))
    handle = Entrez.efetch(db="protein", rettype="gb", retmode="text", id=",".join(gi))
    #time.sleep(120)
    for pept in SeqIO.parse(handle, "gb"):
        #print(pept)
        strain=strained(pept)
        if pept.annotations['gi']:
            pept.blast=extra[pept.annotations['gi']]
        else:
            print('Should I have died for a missing gi?')
        #print(strain)
        if strain:
            geneball.setdefault(strain, []).append(pept)
        else:
            geneball['N/A'].append(pept)
    handle.close()

def OLD_mule(hits):
    ticker=0
    breakswitch=99999999999999999
    #breakswitch=10
    timeout=10
    toredo=[]
    gi=[]
    extra={}
    for hit in hits:
        ticker+=1
        if ticker>breakswitch:
            break
        if hit:
            ids=hit[1].split(';')
            for j in ids:
                new=re.search('\|(\d+)\|',j).group(0)[1:-1]
                gi.append(new)
                extra[new]=hit
    print('gi.s to do: '+str(len(gi)))
    try:
        handle = Entrez.efetch(db="protein", rettype="gb", retmode="text", id=",".join(gi))
        #time.sleep(120)
        for pept in SeqIO.parse(handle, "gb"):
            #print(pept)
            strain=strained(pept)
            if pept.annotations['gi']:
                pept.blast=extra[pept.annotations['gi']]
            else:
                print('Should I have died for a missing gi?')
            #print(strain)
            if strain:
                geneball.setdefault(strain, []).append(pept)
            else:
                geneball['N/A'].append(pept)
        handle.close()
    except URLError as e:
        print(e)
        time.sleep(timeout)#snoozies
        toredo=hits
    return toredo

geneball={'N/A':[]}
chunk=500
#seqs=SeqIO.parse(seqfile, 'genbank')
tic=time.time()
with open(hitfile) as file:
    hits= [row for row in csv.reader(file)]
    print(str(len(hits))+' csv lines to process.')
    ###masterbreaker=20
    ####This code is a mess as it is a stack of tweaks to get around server issues...
    for i in range(0,len(hits),chunk):
        print('Lines: '+str(i)+':'+str(i+chunk))
        mule(hits[i:i+chunk])
#print(geneball)
print('strains: '+str(len(geneball.keys())))
gurkin=open(query+'_pickled.dat','wb')
pickle.dump(geneball, gurkin)
toc=time.time()
print('Seconds: '+str(toc-tic))